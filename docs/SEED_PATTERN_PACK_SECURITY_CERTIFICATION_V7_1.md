# Seed and Pattern Pack Security Certification v7.1

## Purpose

Apps can bring Seed Packs and Pattern Mines. This makes Odin much stronger but creates a new trust surface. Certification states prevent seed packs from becoming prompt injection, plugin execution or hidden authority.

## Certification states

```text
trusted_local
review_required
dev_only
blocked
signature_required
quarantined
```

## Certification inputs

- manifest validity;
- schema validity;
- source identity;
- signature or local approval;
- declared capabilities;
- forbidden capabilities;
- prompt-injection scan;
- executable payload scan;
- remote-permission scan;
- app-state mutation scan;
- claim-boundary scan.

## Compile-only rule

Seed and Pattern Packs are declarative inputs. They may shape precompute, QIRC channels, Work Atoms, slots, runtime pack slices and Output Composer patterns. They may not execute code.

## Block conditions

- arbitrary script content;
- hidden prompt to override Odin boundaries;
- request for app apply;
- request for external send;
- request for remote permission grant;
- model or agent authority promotion;
- unbounded seed fanout;
- private data exfiltration pattern;
- license boundary conflict.

## Why Trace

Every accepted Seed or Pattern Pack must contribute a traceable reason for activation. Every blocked pack must produce a safe blocked reason.
