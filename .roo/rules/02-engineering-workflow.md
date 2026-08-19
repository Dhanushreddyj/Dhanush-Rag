# Engineering Workflow

## Before Editing

- Read every allowed file before changing it.
- Treat documentation, ADRs, task registries, prompt registries, review records, and workspace rules as read-only during implementation.
- Confirm referenced fields, functions, classes, imports, and paths actually exist.
- Inspect related tests and startup wiring.
- Compare the task with the current implementation.
- Report a blocker instead of inventing missing architecture.

## Editing

- Use Roo’s file editing tools for source changes.
- Never create source files with `cat >`, heredocs, shell redirection, or Python writer scripts.
- Make the smallest coherent change satisfying the active task.
- Preserve existing behavior outside the task.
- Do not duplicate functions, classes, imports, fixtures, or tests.
- Do not reformat unrelated files.
- Do not remove legacy code unless removal is part of the active task.
- Never repair a corrupted file fragment by fragment; replace it with a clean, reviewed implementation only when authorized.

## Testing

- Use `.venv/bin/python`.
- Run focused tests for the active task first.
- Tests must be deterministic and isolated.
- Unit tests must not require network access, real credentials, LM Studio, AWS, or Qdrant unless explicitly classified as integration tests.
- Do not weaken, skip, or delete tests to obtain a passing result.
- Do not classify exceptions, HTTP 500 responses, warnings, or partial execution as success.
- Run compile checks for changed Python files.
- Run `git diff --check`.
- Inspect the final diff and changed-file list.

## Git and External Actions

Without explicit owner authorization, never:

- commit;
- push;
- merge;
- rebase;
- reset;
- delete branches;
- install dependencies;
- modify environment or secret files;
- make external network mutations.

## Completion Report

Report:

1. concise implementation summary;
2. exact files changed;
3. behavior implemented;
4. tests added or changed;
5. exact commands executed;
6. exact pass/fail results;
7. remaining blockers;
8. confirmation that no out-of-scope files changed.

Never begin another task after completing the report.
