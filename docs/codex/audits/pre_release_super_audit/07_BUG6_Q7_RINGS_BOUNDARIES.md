# Pre-Release Super Audit — Bug6 / Q7 / Rings / Boundaries

| Concept | Status | Risk | Recommendation |
| --- | --- | --- | --- |
| Bug6 | doc_only | Concept exists but release mapping to runtime gates is too implicit. | Add explicit release boundary map in remediation PR. |
| Q7 | doc_only | Multiple Q terms can confuse release reviewers. | Normalize Q7 wording against validators and claim boundaries. |
| rings | implicit_via_gate_or_boundary | Ring-like safeguards are operational but not named as a release map. | Create explicit ring/boundary matrix. |
| candidate_only | implemented | Low; preserve current gates. | Keep validators green. |
| app_owned_apply | implicit_via_gate_or_boundary | Boundary is clear in docs but should be release-indexed. | Add app-owned apply row to release evidence index. |
| local_only | implemented | Low for local deterministic smoke; no public network claim. | Keep endpoint list repo-real. |
| proof | implemented | Proof continuity is spread across reports. | Cross-link proof packets. |
| receipt | implemented | Receipt-to-release narrative is partial. | Add receipt closure map. |
