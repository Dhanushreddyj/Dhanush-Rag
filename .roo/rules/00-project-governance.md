# Project Governance

## Project

This repository contains the independently deployable Python AI service for the Nofeez worldwide real-estate platform.

It does not own:

- the Next.js backend;
- the web application;
- the mobile application;
- unrelated product infrastructure.

The initial production capability is Agentic RAG, built as the foundation of a larger enterprise AI platform.

## Authority Order

Follow this order:

1. Explicit owner and principal-architect decisions.
2. Accepted ADRs.
3. `docs/ARCHITECTURE.md`.
4. `docs/MASTER_CONTEXT.md`.
5. `docs/PROJECT_VISION.md`.
6. `docs/TASKS.md`.
7. `docs/PROMPTS.md`.
8. `docs/REVIEW.md`.
9. Project engineering standards.
10. Workspace rules.
11. `.roo/rules/99-active-task.md`.

If two authoritative sources conflict, stop and report the conflict. Do not guess which one should win.

## Execution Authority

- Only the task in `99-active-task.md` is executable.
- Work on one logical task at a time.
- Never begin the next task automatically.
- Never expand the active task to fix adjacent problems.
- Never modify a file not listed in the active task.
- If another file is required, stop and explain why.
- Repository cleanup must happen through explicitly approved cleanup tasks.
- The Nofeez knowledge-base requirements supplement the platform architecture; they do not authorize an unreviewed redesign.
- Governance documents and workspace rules are read-only during implementation. They are maintained by the owner and principal architect, not by coding agents.
