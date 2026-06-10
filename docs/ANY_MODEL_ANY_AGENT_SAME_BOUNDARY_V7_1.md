# Any Model / Any Agent / Same Boundary v7.1

## Canon
Any model. Any agent. same Odin boundary.

## Boundary components
- capability card
- permission card
- work capsule
- output contract
- return contract
- claim boundary
- semantic diff
- why trace
- final gate
- app-owned apply

## Consequence
Odin does not care whether a worker is small, large, local, remote, hosted, coding-oriented, browser-oriented or workflow-oriented. Odin cares about what the worker is allowed to receive, what it is allowed to return, what claims it may make, and whether the app must review before apply.

## Anti-patterns
Direct tool execution, direct app apply, prompt-only delegation, unstructured remote context dumps, hidden multi-agent consensus, model-as-authority, agent-as-receipt, and unreviewed external sends are invalid.


## Non-negotiable red lines
- Any model. Any agent. same Odin boundary.
- No worker may become app authority.
- No worker may perform app apply.
- No worker may perform external send through Odin.
- No adapter may bypass Odin Final Gate.
- No remote worker may receive raw private context unless explicitly allowed by privacy class and caller policy.
- No tool-using agent may execute tools through Odin unless a Permission Card allows the exact candidate operation.
- All outputs remain Candidate Artifacts, Review Notes, Risk Notes, PatchPlan Candidates, Handoff Returns, or Receipt Candidates.
- Thor discipline remains candidate-only and kernel-bound.
- GPL-2.0-only is the repository license identity for Odin and expected sibling identity for Thor when distributed together.
