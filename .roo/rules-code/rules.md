# Code Mode Execution Rules

Code mode performs implementation only when the active task is explicitly authorized by the repository governance documents.

Governance documents and workspace rules are read-only in Code mode. Code mode may generate or modify only source and test files explicitly authorized by the active task.

Before editing:
1. Read `.roo/rules/99-active-task.md`.
2. Read the governing task and prompt entries in `docs/TASKS.md` and `docs/PROMPTS.md`.
3. Inspect every allowed file.
4. Confirm that the task status is executable and that the documents do not contradict each other.

During implementation:
- Modify only files explicitly allowed by the active task.
- Make the smallest change satisfying the acceptance criteria.
- Preserve approved architecture and public behavior.
- Never invent files, fields, functions, APIs, dependencies, or requirements.
- Use Roo editor tools for source-code changes.
- Never create source files using shell heredocs, `cat >`, `echo >`, or Python writer scripts.
- Never perform unrelated cleanup or refactoring.
- Never weaken tests to make them pass.
- Never expose or modify secrets.
- After two failed attempts using the same approach, stop and report the failure instead of repeating it.

Verification:
- Run only the focused checks required by the active task.
- Report exact commands and complete results.
- Report every changed file.
- Run `git diff --check`.
- Inspect the final diff before declaring completion.

Git:
- Do not stage, commit, push, merge, rebase, reset, or delete branches unless the owner explicitly requests that exact action.

Stop after completing the active task. Never automatically begin the next task.
