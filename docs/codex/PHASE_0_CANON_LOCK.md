# Phase 0 — Canon Lock

## Goal

Make repository self-describing and impossible to misread before runtime implementation begins.

## Tasks

- Verify root entrypoints.
- Verify Master Architecture and Master Specs exist and include v7.1 laws.
- Verify SYSTEM_MAP points to all canonical docs.
- Verify FILE_MANIFEST generated.
- Verify schema/registry JSON valid.
- Verify no unsupported positive claims outside allowed boundary docs.

## Done

`python -m odin.cli validate-all` OK and `pytest -q` OK.
