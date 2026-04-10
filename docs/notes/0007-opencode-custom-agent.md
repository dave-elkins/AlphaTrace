# 0007 - OpenCode Custom Agent

**Date:** 2026-04-10

## Session Objective

Built a reusable custom command and agent in OpenCode to generate session notes. Created a `/session-note` command that invokes a `session-note` subagent to document development sessions for blog content.

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Agent config location | Both `.opencode/agents/session-note.md` and `.opencode/config.json` | Both needed - config.json for JSON schema, markdown for agent definition |
| Permission strategy | `write: ask` | Provides user control over file creation |
| Agent mode | subagent | Properly invoked via Task tool from command |

## Trade-offs Considered

- **Single file vs dual config**: Initially tried only config.json, but OpenCode requires markdown agent file in `agents/` directory
- **Write allow vs ask**: Chose ask permission for user control, though write is allowed in config

## Concept Design / WYSIWID Observations

The session-note command demonstrates the **command + agent** pattern in OpenCode:
- Commands (`commands/session-note.md`) provide the template/prompt
- Agents (`agents/session-note.md`) define the executing subagent with permissions
- Both work together - command invokes the agent

## Blog Angles

- "How to create reusable commands in OpenCode"
- "A practical guide to OpenCode custom agents"
- "Building your CLI dev workflow with custom agents"

## Next Steps

- Test the `/session-note` command works end-to-end
- Refine permissions if needed based on testing
- Create other reusable commands as needed