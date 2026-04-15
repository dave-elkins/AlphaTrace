# 0005 - Enhancing Vision with AI Techniques

**Date:** 2025-04-10

## Session Objective

Reviewed research chat on focused investing and AI company analysis techniques. Added new AI capabilities to vision and candidate concepts docs without requiring expensive external data purchases.

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Add AI techniques table | Yes (002-vision.md) | Shows technical capability without cost |
| Enhance ChecklistAudit | Yes (003-candidate-concepts.md) | Integrates AI due diligence into existing concept |
| Skip alternative data | Yes | Would require spending money on data providers |
| Use prompt engineering approach | Yes | Free, demonstrates meaningful AI skill |

## Trade-offs Considered

- **Alt Data vs. Prompt Engineering**: Satellite imagery, credit card data offer alpha but cost money. LLM-based analysis of earnings calls uses public filings — free but requires skill
- **New Concept vs. Extension**: Could create `MoatAudit` concept or extend `ChecklistAudit`. Chose extension to avoid concept sprawl
- **Wrapper detection**: The "wrapper test" (would company value disappear if OpenAI released an update?) is clever but hard to automate — kept as human checklist item

## Concept Design / WYSIWID Observations

The AI Due Diligence sub-assessment extends the existing `ChecklistAudit` concept rather than creating a new one. This follows the WYSIWID principle — a single concept that does one thing well. The moat assessment already existed; we just added AI-specific criteria.

New misfit identified: Analyzing CEO speech patterns for "evasiveness" requires NLP analysis that existing concepts don't cover. This could eventually become a sync rule:
> `When Analysis.run → NLPAnalysis.analyze(earnings_transcript)`

## Blog Angles

- "AI Without the Price Tag" — How to demonstrate AI skills without buying expensive datasets
- The "Wrapper Test" — Detecting if a company is AI-first or AI-washing
- Prompt Engineering > Data Buying — Why skill beats spend

## Next Steps

- Consider sync rule for NLP analysis of earnings transcripts
- Explore implementing one of the AI techniques (e.g., code-base analysis via GitHub API)
- Continue with concept implementation phase