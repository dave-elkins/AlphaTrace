# Candidate Concepts

This document outlines the candidate concepts for AlphaTrace, organized by functional domain. Each concept is described at a high level — this is not a formal definition, but a starting point for further refinement during implementation.

## Data Layer

### Company

The core entity representing a publicly traded company.

- **State**: ticker symbol, company name, sector, industry, business description
- **Purpose**: Single source of truth for company identity. All other concepts reference a Company by its ID (uninterpreted atom).

### FinancialMetrics

Quantitative financial data fetched from public sources (yfinance).

- **State**: ROE, Owner Earnings, Debt-to-Equity ratio, free cash flow, operating cash flow, book value per share, shares outstanding
- **Purpose**: Stores the "hard numbers" from Buffett-style analysis. Updated periodically or on-demand. Shares outstanding used for market cap calculation.

### MarketData

Daily market price data for a company.

- **State**: ticker, date, open, high, low, close, adjusted_close, volume, market_cap
- **Actions**: fetch_historical(company_id, start_date, end_date), get_price_at(company_id, date), get_current(company_id)
- **Purpose**: Provides historical and current pricing data for valuation and outcome tracking. Market cap fetched directly from yfinance.

### Dividend

Dividend payment history for a company.

- **State**: company_id, ex_dividend_date, amount_per_share
- **Actions**: fetch_for_company(company_id), get_dividends_between(company_id, start_date, end_date)
- **Purpose**: Tracks dividend payments for total return calculation. Used with MarketData to compute actual investment returns over time.

---

## Analysis Layer

### IntrinsicValue

Discounted Cash Flow (DCF) valuation for a company.

- **State**: fair value estimate, growth rate assumption, discount rate (WACC), terminal growth rate,DCF model inputs/outputs
- **Purpose**: Calculates the "fair value" of a business based on cash flow projections. The operational principle: fair value must be recalculated when key assumptions change or new financial data arrives.

### MarginOfSafety

The cushion between intrinsic value and market price.

- **State**: target buy price, margin of safety percentage, current MOS status (overvalued/fair/undervalued)
- **Purpose**: Determines whether a stock trades at a price that provides adequate protection. Tracks when price drops below the Margin of Safety threshold.

### InvestmentMemo

A point-in-time investment recommendation for a company.

- **State**: 
  - company_id, created_at, finalized_at
  - recommendation (BUY / PASS / HOLD / SELL)
  - target_price (from MarginOfSafety at finalization)
  - confidence_level (0-100, derived from ChecklistAudit + BiasAudit)
  - linked_artifacts (thesis_id, pre_mortem_id, checklist_id, bias_audit_id, intrinsic_value_id, margin_of_safety_id)
  - user_notes
  - outcomes: list[OutcomeSnapshot]
  - archived
- **Actions**: create(company_id), finalize(), archive(), review()
- **Purpose**: Consolidates all analysis artifacts into a recommendation snapshot. Enables learning by tracking actual outcomes against predictions at 1yr, 3yr, 5yr, 10yr horizons.
- **Operational Principle**: A finalized memo is immutable. To update your view on a company, create a new memo.

#### OutcomeSnapshot

- **State**: horizon (1yr / 3yr / 5yr / 10yr), actual_return, benchmark_return, outcome (OVERPERFORMED / UNDERPERFORMED / MEETS_EXPECTATIONS), calculated_at
- **Purpose**: Records actual performance at each milestone. Used for bias learning and analysis accuracy review.

---

## Portfolio Layer

### Watchlist

A list of companies being monitored for potential investment.

- **State**: list of Company IDs, notes, tags, date added
- **Purpose**: Tracks companies of interest. Shows Margin of Safety status for each. Sync rule: when IntrinsicValue recalculates, update MarginOfSafety for all watched companies.

### Position

A current holding in the portfolio.

- **State**: Company ID, number of shares, average cost basis, position size (% of portfolio), date acquired
- **Purpose**: Represents an actual investment. Enforces position size limits (no single holding too large).

### Portfolio

The collection of all positions.

- **State**: list of Position IDs, total value, cash position, rebalancing rules
- **Purpose**: Manages the focused portfolio as a whole. Enforces the 10-30 stock limit. Calculates allocation percentages.

---

## Document Layer

### InvestmentThesis

A structured investment case for a company.

- **State**: bull cases (3), kill-switch sell conditions (3), thesis text, date created, author
- **Purpose**: Documents the "why" behind an investment. Generated AI-assisted but owned by the user.

### PreMortem

A forward-looking failure analysis.

- **State**: failure scenarios (5-year outlook), risk factors, mitigation notes, identified_biases[], lollapalooza_score (1-10), kill_switch_metric, kill_switch_threshold
- **Purpose**: Forces confrontation of downside before buying. Part of the disciplined investment process. Tracks which psychological biases were identified at time of analysis.

### ChecklistAudit

A structured vetting checklist.

- **State**: Circle of Competence assessment, Moat assessment (includes AI Due Diligence), Management assessment, Financials assessment, Valuation assessment, overall pass/fail
- **Purpose**: Provides binary go/no-go decision framework. Each category is scored.

#### AI Due Diligence (Moat sub-assessment)

- **Data Sovereignty** — Proprietary data ownership, flywheel effect, data freshness
- **Architecture** — Built-in vs. bolt-on AI, compute efficiency, "wrapper" test (if OpenAI/Google released an update, would the value proposition disappear?)
- **Talent & Execution** — Key personnel, open source contribution, shipping velocity
- **Unit Economics** — Margin expansion since AI implementation, revenue per employee, CAC impact

#### Moat Strength Assessment

| Feature | Low Moat (Vulnerable) | High Moat (Defensible) |
|---------|----------------------|------------------------|
| Model | General-purpose public LLM | Custom-tuned/private model |
| Data | Web-scraped/public data | Proprietary/sensor/user data |
| Switching Cost | Easy to leave; no lock-in | AI integrated into client's workflow |
| Margins | High API costs eat profit | High efficiency; proprietary hardware/SLMs |

---

## Psychological Defense Layer

### BiasAudit

A structured assessment of cognitive biases affecting a decision.

- **State**: decision_type (buy/sell/hold/feature), detected_biases (BiasType enum: SOCIAL_PROOF, AUTHORITY_BIAS, SUNK_COST, ANCHORING, CONTRAST_MISREACTION, DEPRIVAL_SUPER_REACTION, LIKING_LOVING, AVAILABILITY_MISWEIGHTING, CONFIRMATION_BIAS, OVEROPTIMISM), severity_scores (1-10 per bias), evidence_snippets, lollapalooza_detected (bool), lollapalooza_score (1-10), bias_adjusted_confidence (1-100)
- **Purpose**: Documents which psychological tendencies are influencing the decision. Triggered automatically when analyzing investment theses or feature requests.

### DecisionLog

A historical record of all decisions made through AlphaTrace.

- **State**: decision_id, timestamp, context (STOCK_PM / PRODUCT_ANALYST), decision_summary, user_confidence (1-100), agent_confidence (1-100), actual_outcome (OVERPERFORMED/UNDERPERFORMED/MEETS_EXPECTATIONS), post_hoc_analysis
- **Purpose**: Enables the system to learn which biases the user is most prone to over time. The operational principle: the system should adjust its bias weights based on historical accuracy.

### AgentPersona

Configuration for the AI agent's behavioral mode.

- **State**: persona_type (CONTRARIAN / RATIONAL_ARCHITECT / ANTAGONIST_AUDITOR / COUNCIL_MODERATOR), system_prompt, bias_sensitivities[], output_format
- **Purpose**: Allows swapping between different analytical personas depending on the decision context.

---

## Cross-Cutting Concepts

### Alert

Notifications for important events.

- **State**: alert type (price_drop, recalculation_needed, target_hit), Company ID, triggered_at, acknowledged
- **Purpose**: Keeps the user informed. Examples: "AAPL dropped 10% — time to check Margin of Safety", "NVDA earnings report — recalculate Intrinsic Value".

---

## Cross-Concept Relationships

### Sync Rules (Draft)

1. **When FinancialMetrics.update → IntrinsicValue.recalculate**
   - New financial data means DCF assumptions may need updating

2. **When IntrinsicValue.update → MarginOfSafety.recalculate**
   - Fair value changed → Margin of Safety must be recomputed

3. **When MarketData.update → MarginOfSafety.recalculate**
   - Current price changed → Margin of Safety must be recomputed

4. **When Position.add → Alert.price_drop.subscribe**
   - Start monitoring for price drops on new positions

5. **When InvestmentMemo.create → generate empty artifacts**
   - Create placeholder InvestmentThesis, PreMortem, ChecklistAudit, BiasAudit linked to this memo

6. **When InvestmentMemo.finalize → lock in recommendation**
   - Requires all linked artifacts to be complete
   - Stores target_price from MarginOfSafety at time of finalization
   - Records linked artifact IDs (thesis_id, pre_mortem_id, etc.)

7. **When InvestmentMemo.finalize → DecisionLog.record**
   - Log decision for bias learning

8. **When InvestmentMemo.outcomes.triggered (1yr/3yr/5yr/10yr) → calculate outcome**
   - Fetch price at finalization from MarketData
   - Fetch price at outcome date from MarketData
   - Fetch dividends between dates from Dividend
   - Calculate total return and store OutcomeSnapshot

9. **When DecisionLog.recorded → update BiasProfile**
   - After any decision, update the user's personal bias vulnerability scores

10. **When DecisionLog.outcome_received → adjust BiasWeights**
    - When actual outcome is known, adjust which biases the system penalizes more heavily based on what the user got wrong

11. **Guard: Position.add provided ChecklistAudit.pass**
    - Cannot add to portfolio without passing checklist

12. **Guard: Position.add provided BiasAudit.Lollapalooza_Score < 7**
    - Cannot add to portfolio if Lollapalooza score is 7 or higher (multiple biases converging)

13. **Guard: Position.add provided Portfolio.size_limit_not_exceeded**
    - Cannot exceed 30 stocks in focused portfolio

### Data Flow

```
yfinance → FinancialMetrics → IntrinsicValue → MarginOfSafety
                  ↓                                    ↓
              MarketData ──────────────────────→ MarginOfSafety
              Dividend ─────────────────────────→ (for total return)

Company + Metrics + IntrinsicValue + MOS → InvestmentMemo
                                          ↓
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
           InvestmentThesis         PreMortem           ChecklistAudit
                                                  ↓
                                            BiasAudit
                                         (Psychological Layer)

Position ──────────────────────────────→ DecisionLog ← BiasAudit
Position ────────────────────────────────→ Alert
InvestmentMemo ────────────────────────→ OutcomeSnapshot
                           (MarketData + Dividend)
```

**Psychological Layer Flow:**

```
InvestmentMemo.finalize → BiasAudit.generate → Lollapalooza detection
                                            ↓
                          DecisionLog.recorded → BiasProfile
                                            ↓
                          DecisionLog.outcome_received → BiasWeights.adjust
```

---

## Open Questions

1. ~~**Versioning**~~: Resolved — each InvestmentMemo creates fresh artifacts (new thesis_id, pre_mortem_id, etc.). No version history within concepts.

2. **Alert delivery**: How should alerts be delivered? CLI notifications only? File-based? Extensible to email/webhook?

3. ~~**AI provider**~~: Resolved — infrastructure concern, not a domain concept.

4. **Data freshness**: How often should MarketData refresh? On-demand only, or background polling for watched companies?

5. **Bias weights**: Should bias severity weights be global or personalized? The chat suggests personalization ("if you always fall for Sunk Cost, it gets a 1.5x multiplier"). How do we bootstrap this for a new user?

6. **Lollapalooza threshold**: The draft guard uses Lollapalooza_Score < 7. Is this the right threshold? Should it be configurable per user?

7. **Multi-agent execution**: The "Council of Contrarians" requires running multiple agent sub-tasks. Is this done via parallel LLM calls? Sequential? A multi-agent framework (AutoGen, CrewAI)?

---

## Next Steps

When implementing, start with:

1. **Company** — the simplest starting point, establishes the ID system
2. **FinancialMetrics + MarketData + Dividend** — demonstrate fetching external data, historical prices, and dividend data
3. **IntrinsicValue** — introduces the core mathematical model

These establish the data layer foundation. The portfolio and document concepts build on top.
