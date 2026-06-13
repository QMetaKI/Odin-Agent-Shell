# FINAL-PR-13: Odin Agent Operator Work Packet

**Claim boundary:** final_pr_13_v1_candidate_release_closure_not_external_release  
**candidate_only:** true  
**app_owned_apply:** true

---

## Work Packet

```json
{
  "packet_kind": "odin_agent_operator_work_packet",
  "candidate_only": true,
  "app_owned_apply": true,
  "claim_boundary": "final_pr_13_v1_candidate_release_closure_not_external_release",
  "agent": "claude-code",
  "task": "FINAL-PR-13: v1.0 Candidate Release Closure + Root Public Surface Cleanup",
  "allowed_files": [
    "odin/v1_release_closure/",
    "odin/root_public_surface/",
    "odin/readme_v1/",
    "odin/donation_surface/",
    "odin/release_artifact_boundary/",
    "odin/cli.py",
    "odin/local_hub/server.py",
    "odin/local_hub/ui.py",
    "README.md",
    "DONATIONS.md",
    "tools/rebaseline/check_final_pr_13_v1_release_closure.py",
    "tests/test_final_pr_13_v1_release_closure.py",
    "registries/final_pr_13_*.json",
    "schemas/final_pr_13_*.json",
    "examples/final_pr_13/",
    "reports/final_pr_13_*.json",
    "docs/rebaseline/FINAL_PR_13_*.md",
    "docs/release/FINAL_PR_13_*.md",
    "docs/codex/handoffs/FINAL_PR_13_*.md",
    "docs/codex/audits/FINAL_PR_13_*.md",
    "docs/codex/reports/FINAL_PR_13_*.md",
    "SYSTEM_MAP.json",
    "FILE_MANIFEST.json"
  ],
  "forbidden_actions": [
    "app_state_apply",
    "external_send",
    "hidden_tool_execution",
    "provider_api_call_without_receipt",
    "claiming_proof_without_receipt",
    "domain_state_mutation",
    "tag_creation",
    "github_release_creation",
    "pypi_publication",
    "release_asset_upload",
    "claiming_production_readiness",
    "claiming_security_certification",
    "claiming_external_release"
  ],
  "acceptance_gates": [
    "validate-final-pr-13-v1-release-closure returns 0",
    "validate-all returns 0",
    "pytest suite passes",
    "README.md has all required v1.0 sections",
    "README.md includes exact Thor-Agent-Kit Thank You block",
    "DONATIONS.md exists and references Odin"
  ]
}
```

## Not-Proven List

- production_readiness
- security_certification
- external_release_certification
- live_model_inference
- app_state_mutation
- external_send_authority
