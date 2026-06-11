# Forbidden Control Pattern Registry V1

**Claim boundary:** `forbidden_control_pattern_registry_schema_not_automated_enforcement`

**LRH-PR:** LRH-PR-18  
**Candidate-only:** true  
**Local-only:** true

---

## What This Is

Central registry of forbidden control patterns. Context-aware: scripts/code are strict; docs allow negated boundary phrases (e.g., "no app apply by agent"). Wording and pattern guidance source of truth.

This is not an automated runtime enforcer.

---

## What This Is Not

- Not an automated runtime enforcer
- Not a security certification
- Not production readiness

---

## Categories

| Category | Contexts | Description |
|----------|----------|-------------|
| `app_apply` | scripts, code, agent packets | Direct app state apply by non-app actors |
| `external_send` | scripts, code, agent packets | Unauthorized external data sends |
| `hidden_tool_execution` | scripts, code, agent packets | Undeclared tool execution |
| `public_network_bind` | scripts, code | Public/non-localhost address binding |
| `provider_model_execution` | scripts, code | Live provider/model calls without receipts |
| `windows_service_install` | scripts, code, agent packets | Windows service creation/installation |
| `tray_launch` | scripts, code, agent packets | System tray application launch |
| `installer_creation` | scripts, code | Real installer artifact creation |
| `code_signing` | scripts, code | Actual code signing operations |
| `registry_mutation` | scripts, code | Windows registry mutation |
| `task_scheduler_mutation` | scripts, code | Windows Task Scheduler mutation |
| `admin_elevation` | scripts, code | Administrative elevation requests |
| `destructive_cleanup` | scripts, code | Destructive irreversible cleanup |
| `credential_exfiltration` | scripts, code, agent packets, examples | Credential extraction or exposure |
| `unredacted_support_bundle` | scripts, code | Unredacted sensitive data in bundles |

---

## False Positive Prevention

Docs and reports are allowed to **discuss** forbidden patterns in negated context. Rules must not flag phrases like "no app apply by agent" or "not_production_readiness". Only positive authority claims in wrong context should be flagged.

Safe negation markers: `not `, `no_`, `no `, `never `, `disallowed`, `forbidden`, `blocked`, `not_proven`, `retained_gap`.

---

## Registry Location

`registries/forbidden_control_pattern_registry_v1.json`
