# Public Repo Root Cleanup Policy v7.1

## Purpose

Root documents are the first trust surface of the public repository. They must communicate the current Odin v7.1 canon, not the whole exploratory history.

## Root file responsibilities

- `README.md`: concise public identity, quick start, license, current status.
- `START_HERE.md`: human/operator reading path.
- `CANON_ENTRY.md`: current non-negotiable canon and authority order.
- `CODEX_START_HERE.md`: Codex build path and real PR bundle route.
- `AGENTS.md`: agent behavior contract.
- `CLAIM_BOUNDARY.md`: forbidden claims and status ceiling.
- `CHANGELOG.md`: full chronology.
- `SYSTEM_MAP.json`: machine-readable navigation.
- `FILE_MANIFEST.json`: file inventory and SHA references.

## Allowed in root

- current canonical version;
- public repo identity;
- validation commands;
- hard boundaries;
- links to docs;
- minimal current build sequence;
- GPL-2.0-only notice.

## Not allowed in root

- repeated historical status blocks;
- unscoped feature lists without canonical status;
- runtime proof language;
- product-complete implications;
- vague “AI magic” language;
- ambiguous apply or tool-use language.

## Codex cleanup behavior

Codex may shorten or reorganize root documents if and only if the full canonical content remains in docs, registries, CHANGELOG, SYSTEM_MAP and FILE_MANIFEST. Cleanup must not delete the build canon.
