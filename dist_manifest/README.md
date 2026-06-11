# dist_manifest/

**Claim boundary:** `dist_manifest_static_examples_only_not_generated_build_output_not_release_certification`

This directory contains **static example and spec artifacts** for LRH-PR-15 Portable Packaging and Release ZIP.

## What is here

- `portable_package_manifest.example.json` — example shape of a generated portable package manifest
- `portable_package_release_verification.example.json` — example shape of a local release verification report
- `portable_package_exclusions_v1.json` — static junk exclusion policy spec

## What is NOT here

- Generated build output
- Actual checksums from a real build run
- Real release artifacts
- Signed distribution artifacts

## Where generated output goes

Generated manifests, reports, and ZIP archives are emitted to caller-specified paths during build:

```
python scripts/build_portable_package.py \
  --out /tmp/odin_lrh_pr15_package \
  --manifest-out /tmp/odin_lrh_pr15_manifest.json \
  --report-out /tmp/odin_lrh_pr15_release_verification.json
```

Generated artifacts are **not committed** to the repository.

## Proof boundary

This directory is a portable package candidate artifact.

Not production readiness. Not security certification. Not signed distribution proof.
Not release certification. Not Windows service/tray/installer proof. Not target-host proof.
Not app store readiness. No app apply. No external send.
