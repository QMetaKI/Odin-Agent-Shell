# Local / Remote LLM Parity v7.1

## Parity definition
Local and remote workers share the same candidate protocol, not the same trust level. Parity means same contract shape: Capability Card, Permission Card, Work Capsule, Return Contract, Candidate Artifact, Why Trace.

## Trust difference
Local workers may receive broader local context according to caller policy. Remote workers require explicit permission, redaction, tighter packet size and stronger review.

## Routing discipline
Odin uses deterministic, 1B/2B, 3B, 7B/8B, hybrid and local heavy routes before remote unless caller policy and QMath route score justify remote.

## Expected benefit
This prevents vendor-specific prompt sprawl and lets Odin compare local and remote workers through one visible route score.


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
