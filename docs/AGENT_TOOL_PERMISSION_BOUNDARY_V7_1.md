# Agent Tool Permission Boundary v7.1

## Purpose
Tool-using agents are more dangerous than plain models. Odin therefore treats tool access as a permission-card-controlled candidate surface.

## Permission modes
- read_digest_only
- draft_candidate_only
- review_note_only
- patchplan_candidate_only
- command_preview_candidate_only
- app_apply_required
- blocked

## Tool-use rule
A tool-using agent may propose command previews, patchplan candidates, research notes or risk notes. Odin may not execute those tools on behalf of the agent unless a future explicit app-owned tool gateway exists and the output remains candidate-only.

## Blocked actions
Direct file mutation, direct app apply, external send, purchases, permission changes, credential access, hidden browser operations, background daemon control, network relay expansion, receipt issuance and claim acceptance are blocked.


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
