# Odin SDK Bridge v1

**Version:** 7.1 / LRH-PR-05
**Claim boundary:** sdk_bridge_v1_candidate_only_no_app_apply_no_external_send_no_wan_lan_no_provider_credentials_no_live_model_proof

---

## Purpose

The SDK Bridge v1 provides host apps with a safe, structured way to interact
with Odin's localhost-only API. It exposes only candidate-read and work-submit
surfaces. It never applies app state. It never sends externally.

This is not a public network API.
This does not grant app apply authority.
This does not send externally.
This does not send raw app state to models.
This does not provide provider credentials.
This does not prove live model inference.
This does not prove production readiness.

---

## Python SDK Usage

### Installation

```python
# Import from odin_app_sdk (built-in SDK bridge)
from odin_app_sdk.client import OdinClient, OdinClientError, OdinSDKBoundaryError

# Or import from the standalone SDK module
from sdk.python.odin_client import OdinSDKClient, OdinSDKError, OdinSDKBoundaryError
```

### Basic Usage

```python
from odin_app_sdk.client import OdinClient, OdinClientError

# Default base_url is http://127.0.0.1:8877
# Non-localhost URLs are blocked by default
client = OdinClient("http://127.0.0.1:8877")

# Health check
health = client.health()
assert health["status"] == "ok"
assert health["candidate_only"] is True

# Status
status = client.status()
print(status["candidate_count"], status["session_count"])

# Providers
providers = client.providers()
for provider in providers["providers"]:
    print(provider["provider_id"])

# Submit Universal Work (candidate-only result)
work = {
    "work_id": "MY-WORK-001",
    "work_intent": {"kind": "summarize", "requires_model": False, "goal": "..."},
    "output_contract": {"candidate_only": True, "app_owned_apply": True, "may_apply": False},
    "constraints": {"actions": []},
}
result = client.submit_universal_work(work)
assert result["candidate_only"] is True
assert result["app_owned_apply"] is True
# App owns apply — Odin does NOT apply the candidate

# Read candidate artifact
candidate = client.get_candidate(result["selected_candidate_id"])
assert candidate["candidate_only"] is True
# App decides whether/how to apply this candidate

# Read events
events = client.events()
print(events["events"])

# Read proof gaps
gaps = client.proof_gaps()
print(gaps["proof_boundaries"])
print(gaps["known_gaps"])
```

### Error Handling

```python
from odin_app_sdk.client import OdinClient, OdinClientError, OdinSDKBoundaryError

# OdinSDKBoundaryError is raised for non-localhost URLs
try:
    client = OdinClient("http://192.168.1.1:8877")
except OdinSDKBoundaryError as e:
    print(f"Boundary violation: {e}")

# OdinClientError is raised for HTTP errors, connection errors, timeouts
client = OdinClient("http://127.0.0.1:8877")
try:
    candidate = client.get_candidate("UNKNOWN-ID")
except OdinClientError as e:
    print(f"API error: {e}")
```

---

## TypeScript SDK Usage

The TypeScript SDK is in `sdk/typescript/odinClient.ts`.

```typescript
import { OdinSDKClient, OdinSDKError, OdinSDKBoundaryError } from './odinClient';

// Default baseUrl is http://127.0.0.1:8877
const client = new OdinSDKClient({ baseUrl: "http://127.0.0.1:8877" });

// Health check
const health = await client.health();
console.log(health.status); // "ok"
console.log(health.candidate_only); // true

// Submit Universal Work
const result = await client.submitUniversalWork({
  work_id: "TS-WORK-001",
  work_intent: { kind: "classify", requires_model: false, goal: "test" },
  output_contract: { candidate_only: true, app_owned_apply: true, may_apply: false },
  constraints: { actions: [] },
});
console.log(result.candidate_only); // true
console.log(result.app_owned_apply); // true

// Read proof gaps
const gaps = await client.proofGaps();
console.log(gaps.proof_boundaries);

// Error handling
try {
  const bad = new OdinSDKClient({ baseUrl: "http://192.168.1.1:8877" });
} catch (e: unknown) {
  if (e instanceof OdinSDKBoundaryError) {
    console.log("Non-localhost URL blocked");
  }
}
```

**TypeScript SDK status:** Scaffold available at `sdk/typescript/odinClient.ts`.
Requires a fetch-compatible runtime environment (Node.js 18+, modern browser, Deno).
Does not require npm for deterministic file/content tests.

---

## Health Check

```python
health = client.health()
# Returns:
# {
#   "artifact_kind": "odin_localhost_api_health",
#   "status": "ok",
#   "candidate_only": true,
#   "app_owned_apply": true,
#   "external_send_default": false,
#   ...
# }
```

---

## Submit Universal Work

```python
result = client.submit_universal_work(work, caller_manifest=caller_manifest)
# Returns a candidate-only result.
# Does NOT apply app state.
# Does NOT send externally.
# App owns apply/state/external-send.
assert result["candidate_only"] is True
assert result["app_owned_apply"] is True
assert result["external_send_default"] is False
```

---

## Read Candidate

```python
candidate = client.get_candidate(candidate_id)
# Returns candidate artifact.
# candidate_only: true — Odin does NOT apply this.
# App decides whether to apply.
assert candidate["candidate_only"] is True
assert candidate["app_owned_apply"] is True
```

---

## Read Proof Gaps

```python
gaps = client.proof_gaps()
# Returns proof gap summary.
# Lists what is NOT proven by Odin.
print(gaps["proof_boundaries"])
print(gaps["known_gaps"])
```

---

## Safety Boundaries

The SDK enforces these boundaries automatically:

| Boundary | SDK Behavior |
|----------|-------------|
| localhost-only | Non-localhost URLs raise `OdinSDKBoundaryError` by default |
| no apply() | Method does not exist |
| no external_send() | Method does not exist |
| no provider credentials | No credential parameter in any method |
| candidate-only returns | All work-submit results include `candidate_only: true` |

---

## No apply() Method

```python
# SDK has no apply() method — by design
# App owns apply
assert not hasattr(client, "apply")
```

---

## No external_send() Method

```python
# SDK has no external_send() method — by design
assert not hasattr(client, "external_send")
```

---

## No Credential Defaults

The SDK does not accept, store, or forward provider credentials.
Provider credential management is outside Odin's scope.

---

## Proof Boundaries

```
not_production_readiness_certification
not_windows_service_tray_installer_proof
not_signed_installer_proof
not_live_model_inference_proof
not_model_quality_proof
not_security_certification
not_public_network_api_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_provider_credential_proof
```

---

## CLI Commands

```bash
# Validate localhost API and SDK bridge
python -m odin.cli validate-localhost-api-sdk-bridge

# Run SDK bridge proof (deterministic, bounded)
python -m odin.cli prove-sdk-bridge

# Run all validators
python -m odin.cli validate-all
```

---

## Architecture Reference

See `docs/LOCALHOST_API_CONTRACT_V1.md` for full API specification.
See `docs/MASTER_ARCHITECTURE_V7_1.md` for system architecture context.
See `CLAIM_BOUNDARY.md` for Odin claim boundary policy.
