# 0003 - Candidate Concepts Drafting

**Date:** 2026-04-10

## Session Objective

Created docs/003-candidate-concepts.md outlining the 13 candidate concepts for AlphaTrace, following WYSIWID concept design pattern from AGENTS.md. Drafted README.md structure and content.

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| FinancialMetrics/MarketData | Keep separate from Company | WYSIWID - each concept owns its own state, can evolve independently |
| Document concepts (Thesis/PreMortem/ChecklistAudit) | Keep separate | Allows versioning, edits, distinct lifecycle |
| Concept domains | Data, Analysis, Portfolio, Documents, Cross-Cutting | Matches vision features |
| Sync rules | Documented at high level | Foundation for engine implementation |

## Trade-offs Considered

- **Merged vs separate concepts**: Could merge FinancialMetrics into Company to simplify, but loses independence
- **Persistent vs on-demand documents**: Could generate docs on-demand without storage, but losing versioning limits auditability
- **3 vs more domains**: Could split further, but 5 domains feels balanced for initial implementation

## Concept Design / WYSIWID Observations

- Using "uninterpreted atoms" (Company ID) for cross-concept references - key WYSIWID principle
- Sync rules documented asdraft - will need formal definition during implementation
- Analysis concept as "wrapper" - might be a misfit, may need to revisit (syncs should coordinate, not a central concept)

## Blog Angles

- "From picking tickers to buying businesses" - the philosophy shift
- WYSIWID applied to investment tools - uncommon in fintech
- 13 concepts for 13 ways to think about a stock

## Next Steps

- Implement Company concept first (simplest starting point)
- Set up project structure with uv, pyproject.toml
- Define formal state.yaml for each concept