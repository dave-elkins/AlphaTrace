# 0009 - concept-and-sync-documentation

**Date:** 2026-05-05

## Session Objective

Document all 19 concepts with proper actions sections and remove non-standard "domain" field from concept YAMLs. Create sync specifications showing cross-concept coordination following the WYSIWID pattern.

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Remove "domain" field from concept YAMLs | Remove domain from YAML files, relocate organizational context to README.md | "domain" is not part of the core Concept Design definition; this keeps concept YAMLs aligned with standard principles and easier to maintain |
| Add actions sections to all 19 concepts | Include actions sections with public method signatures (no type annotations) | Concise documentation of concept public interfaces without over-specifying implementation details |
| Structure sync specifications | Adopt when (trigger) / where (guards) / then (invocations + compensating actions) format | Explicitly models cross-concept coordination in a way that maps directly to WYSIWID sync layer rules |
| Location of guards and compensating actions | Restrict to sync layer only, never include in concept code or documentation | Maintains concept isolation; per WYSIWID rules, the sync layer is the sole point of cross-concept coordination |

## Trade-offs Considered

- Keeping "domain" in YAML vs relocating to README (chose README for cleaner, more standard concept definitions)
- Level of detail in actions sections (kept concise with just method signatures, omitting type information to avoid over-specification)
- Number of syncs to document (prioritized 11 core cross-concept interactions to start, with plans to expand coverage later)

## Concept Design / WYSIWID Observations

- Concepts must remain isolated "islands" with no imports between concept packages, as enforced by the project's architectural rules
- All cross-concept coordination lives exclusively in the `syncs/` directory, never inside concept action methods
- Guards (prohibitions on actions) are sync-layer concerns, not embedded in concept logic
- Compensating actions for rollback scenarios belong in sync specifications, not in the concepts that trigger the original action

## Blog Angles

- "Why we removed 'domain' from our concept definitions" (exploring alignment with core Concept Design principles)
- "WYSIWID in practice: How we document cross-concept coordination" (case study of sync spec structure)
- "Building a Concept Design documentation system that scales" (lessons from documenting 19 concepts and their interactions)

## Next Steps

- Verify all 19 concepts have updated actions sections and no remaining "domain" fields in their YAML files
- Review and finalize 11 core sync specifications for accuracy against WYSIWID pattern rules
- Integrate updated concept and sync documentation into project onboarding materials
