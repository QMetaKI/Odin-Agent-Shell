# Public Repo Release Checklist v7.1

## Purpose

This checklist prepares the future public `Odin-Agent-Shell` repository without overclaiming runtime status.

## Required Before Public Repo Initial Commit

```text
Flat root structure verified.
AGENTS.md present.
CODEX_START_HERE.md present.
CANON_ENTRY.md present.
SYSTEM_MAP.json present.
FILE_MANIFEST.json present and current.
Master Architecture present.
Master Specs present.
Deep subsystem specs present.
Internal PR ladder present.
Real PR bundle plan present.
Senior review hardening docs present.
validate-all passes.
pytest passes.
No cache artifacts in ZIP.
No runtime-proof claims.
No provider-key placeholders that look real.
No app template contains LLM runtime.
```

## Public README Boundary Text

The README may say:

```text
Odin Agent Shell is an architecture/specification and build-prep repository for a Windows-first local semantic work kernel and small-model performance OS.
```

The README must not imply:

```text
host validation
model proof
security audit completion
production deployment
applied patch behavior
external network readiness
```

## Codex Launch Rule

After public repo creation, Codex should start with REAL-PR-01 and must not skip to provider/runtime/UI work before foundation gates are green.
