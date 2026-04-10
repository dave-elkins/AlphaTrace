# 0001 - Defining the Idea

**Date:** 2026-04-10

## Session Objective

Define the vision and purpose of AlphaTrace before writing any code. The goal was to create a concise one-pager (`001-idea.md`) that captures what AlphaTrace is and why it exists — serving as the foundational reference for all future development.

## Context

The project began from a development chat where the user explored the **Focused Portfolio** strategy (Warren Buffett-style concentrated investing). Key elements included:
- Quantitative analysis: ROE, Owner Earnings, Margin of Safety, $1 Test
- Qualitative analysis: Moat assessment, Pre-Mortem, Investment Thesis generation
- Python-based automation using `yfinance` for data and LLM APIs for reasoning
- CLI workflow for research, valuation, and portfolio tracking

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Target Audience | Developers | The app serves as a showcase for agentic development capabilities |
| Product Form | CLI-first | Establish the core analytical workflow before adding UI layers |
| Naming | AlphaTrace | Confirmed by the user |

## Trade-offs Considered

1. **CLI vs Web-First**: Starting with CLI allows focusing on domain logic and data processing. A FastAPI layer can be added later for dashboarding.

2. **Developer vs Investor Audience**: While the underlying domain is investment analysis, the user wanted to showcase agentic development skills — so the implementation targets developers who want to extend and customize the workflow.

3. **Feature Scope**: The full vision includes AI-powered qualitative reasoning, psychological bias auditing, and multi-agent debates. We limited the first iteration to the concise idea definition.

## Concept Design / WYSIWID Observations

This session embodies the Concept Design principle from AGENTS.md:

> "Before you write any feature code, you must think in concepts first."

Creating `001-idea.md` is itself an exercise in concept definition at the project level — What is this thing? What is its operational principle? The document answers these before any code is written.

## Blog Angles

- **The Discipline of the One-Pager**: Why start with a vision document? Connecting Concept Design methodology to real-world development workflow.
- **From Investment Strategy to Software Architecture**: How a personal investing philosophy became a showcase for agentic development.
- **Building for Extensibility**: How we scoped the CLI-first to leave room for FastAPI and web UI layers.

## Next Steps

- Generate candidate concepts (state and actions) following the WYSIWID pattern
- Set up the project structure (Python, uv, ruff, ty)
- Implement the first concept (likely `Company` as the simplest starting point)