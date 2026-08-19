# Implementation Quality

- Inspect actual files before editing.
- Modify only files listed by the active task.
- Treat documentation, ADRs, task registries, prompt registries, review records, and workspace rules as read-only.
- Generate or modify implementation and test code only; never perform governance maintenance.
- Preserve existing behavior outside the task.
- Do not duplicate functions, classes, imports, or tests.
- Do not rewrite unrelated files.
- Do not weaken tests to make them pass.
- Use the repository `.venv`.
- Tests must not require real credentials or network access unless explicitly required.
- Run focused tests first.
- Run compile checks for changed Python files.
- Run `git diff --check`.
- Review the final diff before reporting completion.
- Report blockers honestly.
- Do not commit or push unless explicitly instructed.
