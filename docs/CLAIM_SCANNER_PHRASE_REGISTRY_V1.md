# Claim Scanner Phrase Registry V1

**Claim boundary:** `claim_phrase_registry_local_wording_policy_not_automated_scanner`

**LRH-PR:** LRH-PR-18  
**Status:** registry defined  
**Candidate-only:** true  
**Local-only:** true

---

## What This Is

Central registry of claim phrases distinguishing forbidden positive overclaims from allowed negated boundary phrases. Wording policy source of truth for PRs, docs, reports, and code.

This is not an automated runtime scanner.

---

## What This Is Not

- Not an automated runtime scanner
- Not a CI enforcer
- Not a security certification
- Not production readiness

---

## Forbidden Positive Overclaims

Phrases that must not appear as positive assertions in Odin artifacts:

- `fully proven`
- `complete proof`
- `certified`
- `production-ready` (and related production affirmative phrases)
- `guaranteed`
- `security certified`
- `release ready`
- `signed release ready`
- `Windows ready`
- `installer ready`
- `service ready`
- `tray ready`
- `Store ready` / `Microsoft Store ready`
- `target-host proven`
- `production proof`
- `complete`
- `secure`
- `fully implemented`
- `release certified`
- `deployment ready`
- `ship ready`

---

## Allowed Negated Phrases

Phrases explicitly allowed (and required) in boundary docs:

- `not production readiness`
- `not release certification`
- `not security certification`
- `not signed distribution proof`
- `not Windows service proof`
- `not tray proof`
- `not installer proof`
- `not target-host proof`
- `not public network API proof`
- `not live model inference proof`
- `not model quality proof`
- `retained gap`
- `proof gap retained`
- `non-goal boundary`

---

## Allowed Scoped Phrases

- `green` (for local validator pass)
- `passed locally`
- `local receipt`
- `candidate-only`
- `local-only`
- `known non-proof`
- `ok_with_known_gaps`
- `advisory only`

---

## Context-Aware Rules

| Context | Rule |
|---------|------|
| scripts/code | strict — no positive overclaim phrases; negated boundary phrases required |
| docs | allow negated boundary phrases; forbid positive overclaim phrases |
| examples | safe placeholders only; must include `claim_boundary` and `candidate_only` |
| reports | allow negated boundary phrases; require `not_proven` and `proof_boundaries` sections |
| PR bodies | require proof boundary summary; allow scoped positive phrases for local-only results |

---

## Registry Location

`registries/claim_phrase_registry_v1.json`
