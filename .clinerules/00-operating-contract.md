# Project Operating Contract

This repository is an enterprise Python AI platform for real estate.

Follow this authority order:

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
11. `.clinerules/99-active-task.md`.

If sources conflict, stop and report the conflict.

Work on one logical task at a time. The active task defines the only allowed files.

Do not redesign, simplify, replace, or broaden the architecture.

## Cline Role Boundary

Cline is an implementation engineer and code-generation tool only.

- Cline may read governance documents and workspace rules to understand an approved implementation task.
- Cline may edit only source and test files explicitly listed by the active task.
- Cline must not author, revise, promote, or reconcile governance documents, ADRs, task status, controlled prompts, review records, or workspace rules.
- Governance changes are performed by the project owner and principal architect, then reviewed before commit.
- If governance sources conflict, Cline must stop and report the conflict instead of attempting to repair it.
