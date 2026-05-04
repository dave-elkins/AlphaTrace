---
agent: session-note
---

# Session Note

Generates a session note file in `docs/notes/000N-[name].md` capturing what was discussed during the current development session. This is a **documentation-only** task for creating blog post material.

## Usage

`/session-note`

## CRITICAL CONSTRAINTS

- **DO NOT write any code or make any implementation changes**
- **DO NOT create any files outside of `docs/notes/`**
- **DO NOT use the todowrite tool or start any implementation tasks**
- **DO NOT proceed to implementation after creating the note**
- **ONLY create a single markdown file summarizing the session**
- **THIS IS A TERMINAL ACTION** - After writing the note, output a brief confirmation message and STOP. Do not ask follow-up questions, do not proceed with next steps, do not use any other tools.

## Process

1. **Ask for session name** (e.g., "defining-the-idea", "first-concept-implementation")

2. **Ask clarifying questions** (these are for gathering information to write about, NOT for planning implementation):
   - What was the session objective?
   - What decisions were made?
   - What trade-offs did you consider?
   - Any observations relevant to Concept Design or WYSIWID pattern?
   - Anything that might make interesting blog content?

3. **Auto-detect next sequence number**:
   ```
   ls docs/notes/*.md | sort -V | tail -1
   ```
   Extract the number from the last file (e.g., `0001` → `0002`)

4. **Write ONLY the session note** to `docs/notes/[NEXT]-${session_name}.md` using this template:

   ```markdown
   # [SEQUENCE] - [Session Name]

   **Date:** [YYYY-MM-DD]

   ## Session Objective

   [What was accomplished]

   ## Key Decisions

   | Decision | Choice | Rationale |
   |---------|--------|-----------|
   | ... | ... | ... |

   ## Trade-offs Considered

   - [Trade-off 1]
   - [Trade-off 2]

   ## Concept Design / WYSIWID Observations

   [How this session relates to Concept Design principles]

   ## Blog Angles

   - [Hook 1]
   - [Hook 2]

   ## Next Steps

   - [Next step 1]
   - [Next step 2]
   ```

## Example

Session name: "defining-the-idea"
- Last file: `docs/notes/0001-defining-the-idea.md`
- Next file: `docs/notes/0002-setup-project-structure.md`

## What This Command Does NOT Do

- Does NOT implement any code
- Does NOT create todo lists
- Does NOT modify any files outside `docs/notes/`
- Does NOT set up project structure
- Does NOT write tests
- Does NOT ask follow-up questions after note creation
- Does NOT proceed to implementation

This command is purely for **documenting** what was discussed for future reference and blog content. It is a **terminal action** that ends after the note is written.