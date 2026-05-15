---
description: Breakdown Epic into ordered Task Beads for development
agent: build
---

# Persona

You are a Technical Lead. Decompose an Epic Bead into a deterministic sequence of Task beads,
each scoped to exactly one concept or sync rule. Enforce Concept Design and WYSIWID patterns.

# Activities

- Read Epic bead and parse its structured description (Goal, JTBD, AC, Concepts, Syncs, Guards, CLI, Demo)
- Create one Task bead per concept, one per sync rule, one for CLI wiring, one for end-to-end verification
- Assign acceptance criteria scoped to each individual bead
- Chain beads with `bd dep` so the work order is deterministic
- Handle edge cases: infrastructure-only epics, missing YAML specs, guards

# Prompt

Decompose Epic Bead **$BEADID** into Task beads.

## Steps

### 1. Read the Epic

```bash
bd show $BEADID --json
```

Extract these sections from the description:

| Section | Content |
|---------|---------|
| Title | Bead title (first line) |
| Acceptance Criteria | `## Acceptance Criteria` bullet list |
| Concepts | `## Concepts to Implement` table (Name, YAML Spec, Description) |
| Sync Rules | `## Sync Rules to Implement` table (Name, YAML Spec, Trigger → Action) |
| Guards | `## Guards` section |
| CLI Commands | Code block under `## CLI Commands` |
| Demo Script | Code block under `## Demo Script` |

For Concepts and Sync Rules, parse each table row to get the Name and YAML Spec path.

> If the Concepts table says "None" or is absent, this is an infrastructure-only epic (see Step 3).

### 2. Create Task Beads (in exact order)

Create beads **one at a time**, saving each ID into a shell variable. Use `--silent` to capture only the ID.

```bash
# Accumulator for concept bead IDs (needed for CLI bead dependency)
CONCEPT_IDS=""
```

#### 2a. Concept Implementation Beads

For each row in the Concepts table, in table order:

1. Read the YAML spec file at the path from the table (e.g., `docs/concepts/company.yaml`)
2. Create a task bead:

```bash
DESC=$(cat <<'ENDDESC'
[Copy the YAML spec content inline]

## YAML Spec
[docs/concepts/<name>.yaml]

## Purpose
[from YAML: purpose]

## State
[from YAML: state fields]

## Actions
[from YAML: actions]

## Operational Principle
[from YAML: operational_principle]
ENDDESC
)

AC=$(cat <<'ENDAC'
- [ ] Implement all state fields from the YAML spec
- [ ] Implement all actions from the YAML spec as public async methods returning ActionRecord
- [ ] Unit tests cover every action (nominal + error cases)
- [ ] `ruff` linting passes
- [ ] `ty` type checking passes
- [ ] Concept does NOT import from any other concept module
ENDAC
)

BEAD_ID=$(bd create "Implement <ConceptName>" \
  --parent $BEADID \
  --type task \
  --description "$DESC" \
  --acceptance "$AC" \
  --labels "task,concept,role:implementer" \
  --silent)

echo "Created bead $BEAD_ID — Implement <ConceptName>"
CONCEPT_IDS="$CONCEPT_IDS $BEAD_ID"
```

#### 2b. Sync Rule Implementation Beads

For each row in the Sync Rules table, in table order:

1. Read the YAML spec file (e.g., `docs/syncs/on_<trigger>_<action>.yaml`)
2. Identify which concept beads this sync rule connects (source concept = trigger, target concept = action)
3. Look up their bead IDs from the `CONCEPT_IDS` list
4. Build the `--deps` string pointing to those concept beads
5. Create a task bead:

```bash
DESC=$(cat <<'ENDDESC'
[Copy the YAML spec content inline]

## YAML Spec
[docs/syncs/<name>.yaml]

## Trigger
<Concept.action> — bead ID: <SOURCE_BEAD_ID>

## Action
<Concept.action> — bead ID: <TARGET_BEAD_ID>

## Conditions
[from YAML: where conditions]

## Compensating Action
[from YAML: compensating_action]
ENDDESC
)

AC=$(cat <<'ENDAC'
- [ ] Sync rule registered with sync engine
- [ ] When trigger action completes, target action is called with correct args
- [ ] Conditions are checked before firing
- [ ] Compensating action handles rollback correctly
- [ ] Unit tests verify the sync fires and does not fire when conditions aren't met
- [ ] `ruff` and `ty` pass
ENDAC
)

DEPS_STRING="$(echo $SOURCE_BEAD_ID $TARGET_BEAD_ID | tr ' ' ',')"

BEAD_ID=$(bd create "Sync: <TriggerAction> → <TargetAction>" \
  --parent $BEADID \
  --type task \
  --description "$DESC" \
  --acceptance "$AC" \
  --labels "task,sync,role:sync" \
  --deps "$DEPS_STRING" \
  --silent)

echo "Created bead $BEAD_ID — Sync: <TriggerAction> → <TargetAction>"
```

#### 2c. Guards Bead (if any)

If the Guard section is non-empty (does not say "None"):

```bash
DESC=$(cat <<'ENDDESC'
Implement guards for this epic:

| Guard | Description |
|-------|-------------|
[copy guard rows from the epic]
ENDDESC
)

AC=$(cat <<'ENDAC'
- [ ] Each guard condition is checked before the protected action executes
- [ ] Guard violations produce clear, actionable error messages
- [ ] Guards are registered with the sync engine
- [ ] Tests verify guard blocks and allows correctly
- [ ] `ruff` and `ty` pass
ENDAC
)

BEAD_ID=$(bd create "Guards" \
  --parent $BEADID \
  --type task \
  --description "$DESC" \
  --acceptance "$AC" \
  --labels "task,guard" \
  --deps "$(echo $CONCEPT_IDS | tr ' ' ',')" \
  --silent)

echo "Created bead $BEAD_ID — Guards"
```

#### 2d. CLI Integration Bead

Create a task bead that depends on ALL concept beads:

```bash
DESC=$(cat <<'ENDDESC'
Wire CLI commands from the epic to concept implementations:

[copy the CLI Commands code block from the epic]

Each command must:
- Parse arguments and flags correctly
- Call the appropriate concept action
- Display results in a readable format
- Handle errors gracefully
ENDDESC
)

BEAD_ID=$(bd create "CLI Integration" \
  --parent $BEADID \
  --type task \
  --description "$DESC" \
  --acceptance "All CLI commands from the epic work end-to-end, parse args correctly, and display results" \
  --labels "task,cli" \
  --deps "$(echo $CONCEPT_IDS | tr ' ' ',')" \
  --silent)

echo "Created bead $BEAD_ID — CLI Integration"
CLI_ID=$BEAD_ID
```

#### 2e. Verification Bead

Create a verification bead that depends on the CLI bead:

```bash
DESC=$(cat <<'ENDDESC'
Run the Demo Script from the epic to verify end-to-end functionality.

[copy the Demo Script code block from the epic]
ENDDESC
)

# Convert demo script lines to acceptance checkboxes
AC="Run the demo script steps end-to-end and verify each succeeds:"
# (use the demo script content)

BEAD_ID=$(bd create "Verification" \
  --parent $BEADID \
  --type task \
  --description "$DESC" \
  --acceptance "All demo script steps succeed when executed in order" \
  --labels "task,verification" \
  --deps "$CLI_ID" \
  --silent)

echo "Created bead $BEAD_ID — Verification"
```

### 3. Handle Edge Cases

| Condition | Action |
|-----------|--------|
| Concepts table says "None" or absent | Skip 2a. Create infrastructure task beads instead (see below) |
| Sync Rules says "None" or absent | Skip 2b |
| Guards says "None" or absent | Skip 2c |
| YAML spec file not found at path | Warn but still create the bead with a note: "YAML spec not found at <path> — describe work from epic context" |

**Infrastructure-only epics (e.g. M0):** Instead of concept beads, create these:

```bash
# Bead 1
bd create "Set up Python project" \
  --parent $BEADID \
  --type task \
  --description "Initialize Python project with uv, pyproject.toml, ruff, ty" \
  --acceptance "<acceptance from epic>" \
  --labels "task,infrastructure" \
  --silent

# Bead 2 (depends on bead 1)
bd create "Create app scaffolds" \
  --parent $BEADID \
  --type task \
  --description "Create FastAPI app scaffold, CLI scaffold, sync engine scaffold, SQLite init" \
  --acceptance "<acceptance from epic>" \
  --labels "task,infrastructure" \
  --deps "<BEAD_ID_FROM_STEP_1>" \
  --silent
```

### 4. Update Epic State

```bash
bd set-state $BEADID in_progress --reason "Broken down into task beads"
```

### 5. Output Summary

```bash
echo ""
echo "## Breakdown Complete"
echo ""
bd children $BEADID --pretty
echo ""
echo "Work through beads in the order listed above. Each is blocked until its dependencies are done."
echo "Start with the first bead: bd children $BEADID"
```

## RULES

1. Do NOT write any implementation code.
2. One task bead per concept, one per sync rule — never merge multiple concepts into one bead.
3. Every bead is a child of the epic via `--parent $BEADID`.
4. Use `bd create --silent` to capture bead IDs for dependency chaining.
5. Cross-milestone dependencies are assumed complete — do NOT reference beads from other epics.
6. Always read and inline the YAML spec files — they define the work scope.
7. Sync beads MUST depend on their source AND target concept beads via `--deps`.
8. CLI bead MUST depend on ALL concept beads via `--deps`.
9. Verification bead MUST depend on the CLI bead via `--deps`.
10. Always finish with `bd set-state` and `bd children --pretty` to show the full breakdown.
