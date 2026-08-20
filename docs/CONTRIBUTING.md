# Enterprise AI Platform — Contributing Standard

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Applies To:** Human engineers, ChatGPT/Codex architecture work, Cline/Qwen implementation work, and code review

## 1. Purpose

This project uses documentation and ADRs as executable engineering governance. Contributions must preserve the approved architecture while improving the implementation in small, reviewable steps.

The goal is that a new senior engineer can understand not only what to change but why the surrounding boundaries exist.

## 2. Authority Order

When guidance conflicts, use this order:

1. explicit owner decisions;
2. accepted ADRs;
3. `ARCHITECTURE.md`;
4. `MASTER_CONTEXT.md`;
5. `PROJECT_VISION.md`;
6. `TASKS.md`;
7. `PROMPTS.md`;
8. `REVIEW.md`;
9. engineering standards (`CODE_STYLE.md`, `TESTING.md`, `SECURITY.md`, `API_GUIDELINES.md`, `OBSERVABILITY.md`);
10. workspace rules;
11. active-task restrictions.

Do not silently resolve a material conflict. Escalate it to architecture review and create/supersede an ADR when appropriate.

## 3. Required Workflow

`Requirement -> Architecture Decision -> Scoped Task/Prompt -> Implementation -> Tests -> Code Review -> Merge`

No step is skipped merely because an AI coding agent can generate code quickly.

## 4. Before Starting a Change

Every implementation task must identify:

- problem/requirement;
- architectural responsibility/module owner;
- relevant ADRs/standards;
- files explicitly allowed to change;
- files/areas explicitly out of scope where useful;
- expected behavior and acceptance criteria;
- required tests/verification;
- known constraints/decisions that must not change.

If the task requires a material architecture decision that does not exist, stop implementation and return to the ADR phase.

## 5. Scope Discipline

One task modifies one logical module/concern. Tests for that concern are part of the same logical scope.

Do not:

- rewrite the project in one task;
- move folders merely to make the target tree look cleaner;
- fix unrelated defects opportunistically unless required for the authorized task and explicitly brought into scope;
- add frameworks/providers/databases because they may be useful later;
- broaden a task after discovering a neighboring problem—record it for follow-up instead.

Small, intentional diffs are a quality mechanism.

## 6. AI-Assisted Implementation — Cline/Qwen

Cline using the local Qwen model is the implementation engineer, not the architecture authority.

Every Cline prompt must:

- state that architecture is already approved;
- list relevant governance documents/ADRs;
- state the single logical objective;
- explicitly list files Cline may modify;
- identify prohibited changes;
- define acceptance criteria and required tests;
- require Cline to report blockers rather than redesign;
- require a final summary, files changed, tests executed/results, out-of-scope findings, and diff/review information.

Cline must never independently:

- redesign layers/responsibilities;
- introduce a new framework/provider/vector database;
- bypass provider/repository/application contracts;
- move business logic into controllers/providers/LangGraph;
- edit unspecified files;
- choose a DEFERRED ADR technology;
- claim success without verification.

## 7. Human/Architect Review

Every material implementation change is reviewed for:

- architecture compliance;
- behavioral correctness;
- provider/framework leakage;
- async/concurrency correctness;
- error/security/privacy behavior;
- test quality;
- observability requirements;
- backward/API compatibility;
- embedding/index compatibility when applicable;
- scope discipline.

Review the diff, not only the implementation agent's summary.

## 8. Testing Requirements

All changes must satisfy `TESTING.md` at the appropriate layers.

At minimum:

- changed behavior has tests or a documented reason a higher-level verification is required;
- default tests do not require production credentials/services;
- provider adapters have contract tests;
- API changes have transport/streaming/error tests;
- probabilistic AI behavior changes run relevant evaluations;
- failures are fixed, not normalized as valid outcomes.

## 9. Documentation Requirements

Update documentation when a change affects a public/operational/architectural contract.

An ADR is required or strongly indicated when changing:

- architectural dependency direction/responsibility;
- core framework/provider/vector-store strategy;
- production trust/authentication mechanism;
- streaming wire protocol;
- embedding/index compatibility semantics;
- persistent session strategy;
- production deployment/telemetry architecture;
- another architectural invariant.

Do not rewrite accepted ADR history. Supersede it with a new decision when the architecture changes.

## 10. API and Compatibility

API changes follow `API_GUIDELINES.md`. Breaking external changes require explicit version/migration review.

Embedding/model/index changes follow ADR-006 and cannot be treated as harmless configuration flips when compatibility changes.

## 11. Security and Secrets

All contributions follow `SECURITY.md`.

- never commit credentials/secrets;
- never paste secrets into prompts, fixtures, logs, examples, or error messages;
- do not weaken validation/auth/CORS/rate controls to make local development easier;
- development bypasses/stubs must be explicit and impossible to mistake for accepted production trust behavior.

## 12. Commits and Review Units

Commits should represent coherent changes and use descriptive messages. Avoid mixing formatting-only repository-wide churn with behavior changes.

Do not commit generated caches, local credentials, model artifacts, local vector data, editor state, or developer-machine configuration unless an explicit repository policy says otherwise.

Before review, provide:

- purpose;
- files changed;
- behavior changed;
- tests/commands run and results;
- documentation/ADR impact;
- known limitations/follow-ups.

## 13. Definition of Done

A task is done only when:

1. scope/acceptance criteria are satisfied;
2. architecture/ADR rules remain intact;
3. types/errors/async behavior meet standards;
4. required tests/evaluations pass;
5. API/security/observability impacts are handled;
6. documentation is updated when required;
7. diff has been reviewed;
8. no known blocker is hidden behind a successful local demo.

Production-ready status requires evidence beyond local execution.
