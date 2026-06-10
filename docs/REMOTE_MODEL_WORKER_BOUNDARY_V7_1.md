# Remote Model Worker Boundary v7.1

## Purpose
Remote models may be useful as high-quality candidate workers, but remote execution is never authority. Remote workers receive the smallest sufficient redacted packet.

## Remote worker packet
Remote workers may receive a Context Capsule, Output Contract, Return Contract, Forbidden Claims list, redacted evidence references and a candidate-only task. They should not receive raw app state, secrets, full traces, unredacted private context or apply-capable commands.

## Remote route conditions
Remote route is allowed only when caller policy permits remote, privacy class permits remote, redaction passes, local routes are insufficient, expected gain exceeds cost/risk threshold, and Odin Final Gate remains required.

## Remote return handling
All remote returns are treated as model_projection until Odin validates schema, claims, boundaries, evidence requirements and output contract.


## Non-negotiable red lines
- Any model. Any agent. Same Odin boundary.
- No worker may become app authority.
- No worker may perform app apply.
- No worker may perform external send through Odin.
- No adapter may bypass Odin Final Gate.
- No remote worker may receive raw private context unless explicitly allowed by privacy class and caller policy.
- No tool-using agent may execute tools through Odin unless a Permission Card allows the exact candidate operation.
- All outputs remain Candidate Artifacts, Review Notes, Risk Notes, PatchPlan Candidates, Handoff Returns, or Receipt Candidates.
- Thor discipline remains candidate-only and kernel-bound.
- GPL-2.0-only is the repository license identity for Odin and expected sibling identity for Thor when distributed together.
