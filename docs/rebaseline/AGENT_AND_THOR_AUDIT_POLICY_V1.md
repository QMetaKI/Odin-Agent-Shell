# Agent and Thor Audit Policy V1

**Version:** v1.0 — Established in LRH-PR-03  
**Claim boundary:** agent_and_thor_audit_policy_documentary_candidate_only  
**Status:** Standing policy — applies to all future LRH PRs

---

## Purpose

Every LRH PR (LRH-PR-03 onward) must include a structured audit of:

1. Odin Agent Operator Mode usage
2. Thor communication/handoff usage
3. Executing agent worker (e.g. Claude Code, Codex)
4. Efficiency/quality comparison vs. not using Odin/Thor
5. Suggested optimizations/extensions

---

## Required Audit Sections (per PR Return Report)

### 1. Odin Agent Operator Mode Audit

Include in `docs/codex/reports/LRH-PR-XX_RETURN_REPORT.md`:

```
Odin Agent Operator Mode Audit:
- attempted: yes/no
- commands run:
- packet path(s):
- guard/check/proof results:
- failures:
- classification:
- how it shaped the implementation:
- estimated efficiency gain vs. not using Agent Operator Mode:
- quality gain vs. not using Agent Operator Mode:
- what should be optimized in Agent Operator Mode:
- suggested follow-up:
  - weave into next PR
  - add to LRH backlog
  - append as LRH-PR-18+
```

**Efficiency estimate may be qualitative but must be reasoned:**
- reduced prompt ambiguity
- reduced scope drift
- clearer allowed files
- clearer proof boundaries
- faster return report
- better senior review structure

### 2. Thor Communication/Handoff Audit

```
Thor Communication / Handoff Audit:
- attempted: yes/no
- Thor repo/source:
- core commands run:
- Thor/Y commands run:
- successes:
- failures:
- classification:
- how Thor output shaped the implementation:
- what Thor added beyond the base prompt:
- estimated efficiency gain vs. not using Thor:
- quality gain vs. not using Thor:
- what should be optimized in Thor handoff usage:
- suggested follow-up:
  - weave into next PR
  - add to LRH backlog
  - append as LRH-PR-18+
- proof boundary:
  Thor output was advisory and did not replace Odin repo-real validation.
```

### 3. Agent Worker Audit

```
Agent Worker Audit:
- worker: <Claude Code | Codex | other>
- how the agent used Odin Agent Operator Mode:
- how the agent used Thor:
- what was efficient:
- what was inefficient:
- where prompt/context should improve:
- what should be moved into CLAUDE.md / skills / senior reviewer / senior code reviewer:
- suggested follow-up:
```

---

## Classification of Suggestions

All audit suggestions must be classified:

| Classification | Meaning |
|----------------|---------|
| `weave_into_next_pr` | Small improvement, include in LRH-PR-N+1 |
| `add_to_lrh_backlog` | Worth doing later in existing LRH ladder |
| `append_as_lrh_pr_18_plus` | New PR needed, append after LRH-PR-17 |
| `no_action` | Not actionable, document only |

---

## Authority Order

Audits are documentary. They do not override:

1. Master Architecture v7.1
2. Master Specs v7.1
3. Odin claim boundaries
4. Repo-real source and tests

Thor output is advisory. It does not constitute Odin proof.

Agent worker output is candidate-only. App owns apply.

---

## Implementation Note

This policy is documentary. Deterministic tests for audit completeness may be
added in a later LRH PR if concrete test coverage becomes practical.

---

*claim_boundary: agent_and_thor_audit_policy_documentary_candidate_only*
