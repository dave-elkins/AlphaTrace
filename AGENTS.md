# AGENTS.md — Architecture & Coding Conventions

## Paradigm: Concept Design + WYSIWID

This project follows **Concept Design** (Daniel Jackson, *The Essence of Software*) implemented
via the **WYSIWID** (What You See Is What It Does) structural pattern (Meng & Jackson, Onward! 2024).

Before writing any feature code, you must think in concepts first.

---

## The Mental Model

A **concept** is a standalone unit of functionality that a user can name and understand
independently. Examples: `Post`, `Comment`, `Subscription`, `Label`, `Notification`.

Each concept:
- Has its **own state** (it owns its data — no other concept touches it)
- Exposes **actions** (public async methods that modify state and return an ActionRecord)
- Has an **operational principle** — an invariant it maintains internally
- **Never imports another concept**

Cross-concept coordination happens exclusively in the **sync layer**, not inside concepts.

---

## Directory Structure
```
app/
  adapters/
    routes.py         # FastAPI-Routes
    config.py         # App Config common to FastAPI and CLI 
    ...
  concepts/
    post/
      actions.py      # Public async actions → ActionRecord
      state.py        # Pydantic + DB models (private)
      state.yaml      # Human-readable description of state (sets, relations)
    comment/
      ...
    subscription/
      ...
  syncs/
    on_post_delete.py     # When Post.delete → Comment.delete_for_post(post_id)
    on_post_create.py     # When Post.create → Notification.send(...)
  guards/
    require_subscription.py  # Guard: only allow Post.create if Subscription.active
  views/
    dashboard.py          # View Concept: read-only projection across multiple concepts
  engine/
    sync_engine.py        # The mediator: registers and dispatches sync rules
  main.py                 # FastAPI entry point
  cli.py                  # Click cli entry point
```

---

## Rules — Non-Negotiable

**1. Concepts are islands.**
A concept file must never import from another concept. If you feel the urge to do so,
that's a misfit. Stop and resolve it with a sync rule instead.

**2. Cross-concept references are opaque IDs.**
If `Comment` needs to refer to a `Post`, it stores `post_id: UUID` — not a `Post` object.
This is called an "uninterpreted atom." Never pass a rich object across concept boundaries.

**3. Syncs live in `syncs/`, not in concepts.**
"When X happens, do Y in another concept" always belongs in a sync rule.
The concept that fires the action does not know what happens next.

**4. Actions return ActionRecords.**
Every public action emits a typed record of what happened. This is how the sync engine
knows to trigger downstream rules. Do not use callbacks or direct calls inside actions.

**5. Guards are sync-layer concerns.**
"Only allow action A if condition B is true" is a guard rule registered with the engine.
Do not encode cross-concept guards inside concept action methods.

**6. View Concepts are read-only.**
Views aggregate data across concepts for efficient reads (CQRS-style). They are maintained
by sync rules and expose no mutating actions.

---

## Before You Write Any Code

For any new feature, answer these questions first:

1. **What is the concept?** Can a user name it? What is its operational principle?
2. **What state does it own?** List the sets and relations (describe in state.yaml).
3. **What are its actions?** Name them and describe what state they mutate.
4. **What misfits exist?** Where does this concept need to interact with others?
5. **What sync rules are needed?** Write them in plain English before coding:
   - `When [Concept A].[action] → [Concept B].[action]([args])`
   - `Guard [Concept A].[action] provided [condition from Concept B]`

Only after answering these should you write any implementation code.

---

## Design Moves (Refactoring Vocabulary)

When the design doesn't feel right, use these named moves:

- **Split**: One concept is doing two things → split into two concepts + a sync rule
- **Merge**: Two concepts always move together and have no independent value → merge them
- **Lift**: Logic that maps between concepts is inside a concept → lift it to the sync layer

Name your refactoring commits with these terms (e.g., `refactor: lift label-assignment to sync layer`).

---

## Anti-Patterns to Avoid

- **God concept**: One concept that knows about everything. Split it.
- **Sync logic inside a concept**: An action that calls another concept's action directly. Lift it.
- **Leaky state**: Exposing internal DB models from a concept's public interface. Use `Out` models.
- **Implicit coordination**: Two concepts that share a DB table or global variable. Give each its own state.
- **Hallucinated frameworks**: Do not use "LegibleSync", "@legible-sync/core", or "LegibleEngine" —
  these do not exist. Build the sync engine in `engine/sync_engine.py` following the WYSIWID pattern.

---

## Terminology Quick Reference

| Term | Means in Code |
|------|--------------|
| Concept | `concepts/<name>/` package |
| Action | `async def create(...) -> ActionRecord` |
| State | `state.py` Pydantic + DB models |
| Operational Principle | Assertions/guards inside action methods |
| Synchronization | Rule in `syncs/` |
| Guard/Prohibition | Guard rule in `syncs/guards/` |
| Misfit | A cross-concept dependency that needs a sync rule |
| Uninterpreted Atom | `thing_id: UUID` (never a full object) |
| View Concept | `views/<name>.py` read model |
| Compensating Action | `rollback_with(undo_fn)` on a sync rule |
| Design Move | Split / Merge / Lift refactoring |

---

## Python Project Setup

- MUST use `uv` for managing python version, venv, dependencies, etc.
- MUST use `pyproject.toml` to help configure the python tool set.
- MUST use `ruff` for linting and formatting
- MUST use `ty` for type checking
- MUST use `fastapi`, `alembic`, `pydantic`
- MUST use `sqlite`
