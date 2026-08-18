# Nofeez AI Platform — Controlled Cline Prompt Registry

**Status:** IMPLEMENTATION SUSPENDED
**Version:** 2.0
**Last Updated:** 2026-08-18
**Implementation State:** NO EXECUTABLE PROMPT

## 1. Purpose

This registry controls implementation prompts sent to Cline/local models. The authoritative Nofeez requirements materially changed the V1 scope after CL-001 was prepared.

## 2. Suspension Decision

CL-001 is suspended. Do not execute, resume, commit or merge its implementation until:

1. the requirements alignment is accepted;
2. ADR-012 through ADR-018 are accepted or revised;
3. TASKS.md dependencies are confirmed;
4. the local working tree is inspected and recovered from earlier malformed Cline attempts;
5. a new narrowly scoped prompt is explicitly marked ARCHITECT_APPROVED.

Preserve existing uncommitted local work for review; suspension is not authorization to discard it.

## 3. Prompt Lifecycle

DRAFT -> ARCHITECT_APPROVED -> EXECUTED -> REVIEW -> ACCEPTED or REWORK

Only ARCHITECT_APPROVED prompts are executable.

## 4. Registry

| Prompt | Task | Status | Notes |
| --- | --- | --- | --- |
| CL-001 | Former FND-001 prompt | SUSPENDED | Prepared before canonical Nofeez requirements alignment |
| CL-001-R1 | Revised first implementation prompt | NOT GENERATED | Generate after governance and local-worktree review |
| CL-002+ | Later tasks | NOT GENERATED | One prompt after each accepted review |

## 5. Mandatory Prompt Controls

Every prompt must name one objective, allowed files, prohibited scope, governing ADRs, deterministic tests, required evidence and stop conditions. Cline must use editor-native changes rather than shell-generated source files and must stop after repeated tool or syntax failure.

## 6. Current Rule

Do not send implementation prompts to Cline during this governance review. Documentation inspection and read-only evidence collection remain allowed.
