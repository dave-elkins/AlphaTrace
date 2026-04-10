# Candidate Concepts

This document outlines the candidate concepts for AlphaTrace, organized by functional domain. Each concept is described at a high level — this is not a formal definition, but a starting point for further refinement during implementation.

## Data Layer

### Company

The core entity representing a publicly traded company.

- **State**: ticker symbol, company name, sector, industry, business description
- **Purpose**: Single source of truth for company identity. All other concepts reference a Company by its ID (uninterpreted atom).

### FinancialMetrics

Quantitative financial data fetched from public sources (yfinance).

- **State**: ROE, Owner Earnings, Debt-to-Equity ratio, free cash flow, operating cash flow, book value per share
- **Purpose**: Stores the "hard numbers" from Buffett-style analysis. Updated periodically or on-demand.

### MarketData

Live market data for a company.

- **State**: current price, 52-week high/low, market cap, volume, dividend yield
- **Purpose**: Provides real-time pricing context for Margin of Safety calculations. Refreshed frequently for tracked companies.

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

### Analysis

A wrapper concept that orchestrates the full analysis workflow.

- **State**: links to Company, FinancialMetrics, IntrinsicValue, MarginOfSafety, InvestmentThesis, PreMortem
- **Purpose**: Represents a complete analysis instance. When you run `alphatrace analyze AAPL`, you're creating an Analysis. This concept holds references to all related data and documents.

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

- **State**: decision_type (buy/sell/hold/feature), detected_biases[], severity_scores (1-10 per bias), evidence_snippets, lollapalooza_detected (bool), bias_adjusted_confidence (1-100)
- **Purpose**: Documents which psychological tendencies are influencing the decision. Triggered automatically when analyzing investment theses or feature requests.

### BiasType (Enum)

The set of cognitive biases AlphaTrace detects:

- SOCIAL_PROOF, AUTHORITY_BIAS, SUNK_COST, ANCHORING, CONTRAST_MISREACTION, DEPRIVAL_SUPER_REACTION (Loss Aversion), LIKING_LOVING, AVAILABILITY_MISWEIGHTING, CONFIRMATION_BIAS, OVEROPTIMISM

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

5. **When Analysis.complete → InvestmentThesis.generate (AI)**
   - After analysis runs, generate thesis document

6. **When Analysis.complete → PreMortem.generate (AI)**
   - After analysis runs, generate pre-mortem

7. **When Analysis.complete → ChecklistAudit.generate**
   - After analysis runs, generate checklist

8. **When Analysis.complete → BiasAudit.generate**
   - After analysis runs, identify which cognitive biases are present in the investment case

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

Company + Metrics + IntrinsicValue + MOS → Analysis
                                          ↓
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
           InvestmentThesis         PreMortem           ChecklistAudit
                                                  ↓
                                            BiasAudit
                                         (Psychological Layer)

Position ──────────────────────────────→ DecisionLog ← BiasAudit
Position ────────────────────────────────→ Alert
```

**Psychological Layer Flow:**

```
Analysis.complete → BiasAudit.generate → Lollapalooza detection
                                              ↓
                              DecisionLog.recorded → BiasProfile
                                              ↓
                              DecisionLog.outcome_received → BiasWeights.adjust
```

---

## Open Questions

1. **Versioning**: Should InvestmentThesis, PreMortem, and ChecklistAudit store version history? The vision mentions "flags when intrinsic value needs recalculation" — this could imply storing the assumptions that generated each version.

2. **Alert delivery**: How should alerts be delivered? CLI notifications only? File-based? Extensible to email/webhook?

3. **AI provider**: The vision references "AI generates" — should there be a configurable AIProvider concept to swap between OpenAI, Anthropic, local Llama, etc.?

4. **Data freshness**: How often should MarketData refresh? On-demand only, or background polling for watched companies?

5. **Bias weights**: Should bias severity weights be global or personalized? The chat suggests personalization ("if you always fall for Sunk Cost, it gets a 1.5x multiplier"). How do we bootstrap this for a new user?

6. **Lollapalooza threshold**: The draft guard uses Lollapalooza_Score < 7. Is this the right threshold? Should it be configurable per user?

7. **Multi-agent execution**: The "Council of Contrarians" requires running multiple agent sub-tasks. Is this done via parallel LLM calls? Sequential? A multi-agent framework (AutoGen, CrewAI)?

---

## Next Steps

When implementing, start with:

1. **Company** — the simplest starting point, establishes the ID system
2. **FinancialMetrics + MarketData** — demonstrate fetching external data
3. **IntrinsicValue** — introduces the core mathematical model

These three establish the data layer foundation. The portfolio and document concepts build on top.
