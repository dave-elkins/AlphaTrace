# 0008 - Concept YAML Documentation

**Date:** 2026-05-05

## Session Objective

Create structured YAML documentation for all 19 candidate concepts from `docs/003-candidate-concepts.md` in a new `docs/concepts/` directory. Each concept file must be self-contained with no references to other concepts, syncs, or cross-concept rules.

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| File format | YAML | Structured, human-readable, matches `state.yaml` convention in AGENTS.md |
| Sub-concepts (OutcomeSnapshot) | Nested in parent YAML | Single-purpose sub-type tied to InvestmentMemo lifecycle |
| Sub-concepts (AIDueDiligence, MoatStrengthAssessment) | Standalone files | User confirmed these are independent concepts, not nested under ChecklistAudit |
| ChecklistAudit revision | List of analysis types + completion status | User clarified it tracks "have we done them or not" not detailed sub-assessments |
| Operating principles | Required for all 19 concepts | User mandate - drafted missing principles, confirmed existing ones |
| Sanitization | Remove all concept names, sync rules | Enforces WYSIWID "concepts are islands" rule |
| Opaque IDs (company_id, etc.) | Retained | These are uninterpreted atoms, not concept references |

## Trade-offs Considered

- **Nesting vs standalone files**: OutcomeSnapshot nested (1:1 with memo lifecycle), AIDueDiligence/MoatStrengthAssessment standalone (user confirmed they're independent concepts)
- **Sanitization depth**: Removed concept names from purpose/principle fields but kept domain labels like "Portfolio Layer" (not a cross-concept reference)
- **State representation**: Used simplified field lists rather than full Pydantic schemas (documentation purpose, not implementation)

## Concept Design / WYSIWID Observations

This task enforced the **"Concepts are islands"** rule from AGENTS.md:
- Each YAML file is fully self-contained - no imports, no concept references
- Cross-concept references use only opaque IDs (`company_id`, `position_id`) as uninterpreted atoms
- Sync rules and guards were completely stripped from concept definitions (they belong in `syncs/`, not concepts)
- The sanitization process revealed how easy it is to accidentally couple concepts - the original doc had extensive cross-concept references in purpose statements

## Blog Angles

- "Documenting concepts before coding: why we wrote 19 YAML files first"
- "WYSIWID in practice: how sanitizing concept docs revealed hidden couplings"
- "Concepts are islands: what happens when you force each concept to stand alone"

## Next Steps

- Implement concept state models (`state.py`) following the YAML definitions
- Build the sync engine (`engine/sync_engine.py`) to handle cross-concept coordination
- Create actions (`actions.py`) for each concept following the documented action lists
- Write sync rules in `syncs/` to replace the cross-concept references removed from YAML files
