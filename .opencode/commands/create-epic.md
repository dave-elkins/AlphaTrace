---
description: Create Epic bead for a milestone with full specification
agent: build
---

# Persona

You are a Product Owner. Your job is to translate the milestone specification
from `docs/004-milestones.md` into a well-structured Epic bead.

# Activities

- Read milestone from `docs/004-milestones.md`
- Create Epic bead using `bd create --type epic`
- Include Goal, JTBD, Acceptance Criteria, Concepts, Sync Rules, Guards,
  CLI Commands, and Demo Script in the description
- Validate milestone exists before creating
- Check for duplicates before creating
- Support `--dry-run` to preview

# Prompt

Parse **{{ MILESTONE }}** to extract the milestone number (format: `M0`–`M6`).
Normalize: strip the `M` prefix to get the integer (e.g., `M2` → `2`).

## Steps

### 1. Validate milestone reference

Read `docs/004-milestones.md`. Search for the heading `## Milestone N:` where N
is your extracted number. If the milestone is not found, print all available
milestones (`M0` through `M6`) and abort with an error.

### 2. Check for existing bead

Run `bd list --type epic --json` and check if an epic with the title
`"Epic: Milestone N — <Title>"` already exists. If found, print the existing
bead ID and abort with an error.

### 3. Extract fields from milestone doc

From the milestone's section in `docs/004-milestones.md`, extract:

| Field | Source |
|-------|--------|
| **Goal** | Text after `**Goal:**` |
| **Jobs-to-be-Done** | All JTBD entries in the section (preserve full format: "When I... so that...") |
| **Acceptance Criteria** | All `[ ]` checkbox items |
| **Concepts** | The Concepts table (markdown table) |
| **Sync Rules** | The Sync Rules section (table or text) |
| **Guards** | The Guards section (table or text) |
| **CLI Commands** | The code block under `### CLI Commands` |
| **Demo Script** | The code block under `### Demo Script` |

### 4. Construct bead title

Format: **Epic: Milestone N — <milestone title>**

Example: `Epic: Milestone 2 — Calculate What a Company is Worth`

### 5. Construct description

Build a structured markdown body with these sections:

```markdown
## Goal

[goal text]

## Jobs-to-be-Done

[jtbd entries]

## Acceptance Criteria

[ac items]

## Concepts to Implement

[concepts table]

## Sync Rules to Implement

[sync rules]

## Guards

[guards]

## CLI Commands

[cli commands code block]

## Demo Script

[demo script code block]
```

### 6. Create the bead

```bash
bd create "Epic: Milestone N — Title" \
  --type epic \
  --description "$DESCRIPTION" \
  --labels "epic,milestone:M{N}" \
  --priority "P2" \
  $DRY_RUN_FLAG
```

If `--dry-run` was provided by the user, append `--dry-run` to the command to
preview the bead without creating it.

Map priority by milestone:
- M0 → P3 (infrastructure)
- M1, M2 → P2 (core features)
- M3, M4 → P1 (important features)
- M5, M6 → P0 (critical completion)

### 7. Output

Print the created bead ID prominently so the user can chain it into
`/breakdown-epic $BEADID`.
