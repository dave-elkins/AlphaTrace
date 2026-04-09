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

- **State**: failure scenarios (5-year outlook), risk factors, mitigation notes
- **Purpose**: Forces confrontation of downside before buying. Part of the disciplined investment process.

### ChecklistAudit

A structured vetting checklist.

- **State**: Circle of Competence assessment, Moat assessment, Management assessment, Financials assessment, Valuation assessment, overall pass/fail
- **Purpose**: Provides binary go/no-go decision framework. Each category is scored.

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

8. **Guard: Position.add provided ChecklistAudit.pass**
   - Cannot add to portfolio without passing checklist

9. **Guard: Position.add provided Portfolio.size_limit_not_exceeded**
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

Watchlist ──────────────────────────────→ MarginOfSafety
Position ────────────────────────────────→ Alert
```

---

## Open Questions

1. **Versioning**: Should InvestmentThesis, PreMortem, and ChecklistAudit store version history? The vision mentions "flags when intrinsic value needs recalculation" — this could imply storing the assumptions that generated each version.

2. **Alert delivery**: How should alerts be delivered? CLI notifications only? File-based? Extensible to email/webhook?

3. **AI provider**: The vision references "AI generates" — should there be a configurable AIProvider concept to swap between OpenAI, Anthropic, local Llama, etc.?

4. **Data freshness**: How often should MarketData refresh? On-demand only, or background polling for watched companies?

---

## Next Steps

When implementing, start with:

1. **Company** — the simplest starting point, establishes the ID system
2. **FinancialMetrics + MarketData** — demonstrate fetching external data
3. **IntrinsicValue** — introduces the core mathematical model

These three establish the data layer foundation. The portfolio and document concepts build on top.
