# 0006 - Concept Refinement

**Date:** 2026-04-10

## Session Objective

Review and refine the candidate concepts document (003-candidate-concepts.md) through the lens of Concept Design and WYSIWID pattern. Transformed vague concepts into well-defined ones with clear state, actions, and operational principles.

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Rename Analysis → InvestmentMemo | InvestmentMemo | Analysis was vague - couldn't define clear actions. InvestmentMemo consolidates artifacts into a point-in-time recommendation with clear actions: create, finalize, archive, review |
| Versioning approach | Option B - fresh artifacts per memo | Each memo creates new thesis_id/pre_mortem_id. No version history needed within concepts - each is a snapshot tied to a specific memo |
| BiasType location | BiasAudit state as enum | BiasType is an enum (data type), not a concept. Moved into BiasAudit/state.py |
| AI Provider | Implementation concern | Infrastructure detail (database-like), not a domain concept. Keep out of concept layer |
| MarketData structure | Daily OHLCV | Need historical prices for outcome tracking at 1/3/5/10yr horizons |
| Dividend | Separate concept | Irregular events (not daily), user-nameable, clean separation from price data |
| Outcome calculation | Automatic at milestones | System fetches price + dividends, calculates total return. User sets 1yr/3yr/5yr/10yr horizons |
| Shares outstanding | FinancialMetrics | Quarterly granularity. Market cap fetched directly in MarketData |

## Trade-offs Considered

- **MarketData**: Daily OHLCV vs current snapshot — Chose OHLCV for outcome tracking capability
- **Dividend**: Separate concept vs inside MarketData — Chose separate; irregular events, distinct user query ("what dividends did AAPL pay?")
- **Outcome**: Manual vs automatic — Chose automatic; reduces user burden, enables systematic learning
- **Confidence derivation**: Manual vs derived — Chose derived from ChecklistAudit + BiasAudit (base score - bias penalty + MOS bonus)

## Concept Design / WYSIWID Observations

### Analysis was a Misfit Concept

The original "Analysis" concept violated WYSIWID:
- **State**: "links to Company, FinancialMetrics, IntrinsicValue..." — just references, no owned state
- **Actions**: None clearly defined
- **Operational Principle**: "orchestrates the full analysis workflow" — this is sync layer coordination, not a concept

**Resolution**: Transformed into InvestmentMemo with:
- **Owned state**: recommendation, target_price, confidence_level, outcomes, archived
- **Actions**: create, finalize, archive, review
- **Operational Principle**: A finalized memo is immutable. To update your view on a company, create a new memo. This enables learning: compare predictions to actual outcomes.

### Learning Loop Design

InvestmentMemo creates a feedback loop:
1. Create memo → generate artifacts (thesis, pre-mortem, checklist, bias audit)
2. Finalize memo → locks in target_price, records to DecisionLog
3. At each horizon (1yr/3yr/5yr/10yr) → calculate outcome from MarketData + Dividend
4. Store OutcomeSnapshot in memo
5. Later: DecisionLog.outcome_received → adjust BiasWeights based on what the user got wrong

This is the core of the psychological defense layer: systematic learning from actual outcomes.

## Blog Angles

- **"Why We Removed a Concept"** — When something looks like a concept but isn't. The Analysis case study.
- **"Designing for Learning Systems"** — How outcome tracking creates feedback loops for bias refinement
- **"Concept Design in Practice"** — Real-world WYSIWID pattern application

## Next Steps

- Implement starting concepts: Company, FinancialMetrics, MarketData, Dividend
- Define InvestmentMemo actions and state in more detail
- Consider sync engine architecture for triggering outcome calculations