# Shadow Runtime Policy Engine v7.1

## Purpose

The policy engine is the first authority-preserving gate after binding. It decides whether a Universal Work request is allowed to continue to precompute and route planning.

## Inputs

- Universal Work object
- Binding / caller policy
- Remote permission flag
- Output Contract
- Claim Boundary

## Checks

The near-final policy engine checks:

- candidate-only output
- app apply gate requirement
- forbidden action markers
- forbidden runtime claim markers
- remote route permission
- hidden apply/send/mutate wording

## Forbidden Markers

- `apply`
- `apply_changes`
- `mutate`
- `mutate_project`
- `send`
- `external_send`
- forbidden runtime proof tokens

## Output

`ShadowPolicyDecision` includes:

- `ok`
- `decision_id`
- `allowed_route_classes`
- `blocked_markers`
- `required_gates`
- `app_authority`
- `odin_authority`
- `boundary`

## Codex Conversion

The real implementation target is:

- `odin/core/policy_engine.py`
- `odin/protocol/binding.py`
- `odin/core/claim_boundary.py`

The real implementation may refine matching rules, but it must not weaken candidate-only or app-owned-apply semantics.
