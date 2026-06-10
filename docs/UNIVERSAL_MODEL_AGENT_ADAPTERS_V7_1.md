# Universal Model / Agent Adapters v7.1

## Purpose
Adapters are the only permitted way to connect a model, agent, tool worker or external assistant to Odin.

## Adapter contract
An adapter must expose:
- worker_id
- worker_kind
- local_or_remote
- capability_card_ref
- permission_card_ref
- accepted_input_contracts
- allowed_output_contracts
- forbidden_outputs
- privacy_policy
- tool_policy
- return_contract
- why_trace_policy

## Adapter classes
local_llm_adapter, remote_llm_adapter, coding_agent_adapter, browser_agent_adapter, research_agent_adapter, workflow_agent_adapter, ide_agent_adapter, app_agent_adapter, voice_agent_adapter, document_agent_adapter, game_agent_adapter.

## Adapter boundary
Adapters normalize. They do not grant authority. They do not execute returned code. They do not accept claims. They do not issue receipts. They do not perform app apply.

## Failure behavior
If an adapter cannot produce a valid candidate return, Odin emits an agent_adapter_conflict packet and routes to review or block.


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
