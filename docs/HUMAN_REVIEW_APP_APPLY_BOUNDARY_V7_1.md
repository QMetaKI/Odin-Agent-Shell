# Human Review and App Apply Boundary v7.1

## Purpose

This document clarifies the final authority boundary after Odin produces a candidate.

## Boundary Split

| Layer | Authority |
|---|---|
| Model | projection worker only |
| Odin | candidate preparation, gates, trace |
| Thor | handoff/review packet discipline |
| App | state, apply, send, domain action |
| User / domain owner | final human decision where required |

## Candidate Action Classes

```text
informational_candidate
rewrite_candidate
action_card_candidate
patchplan_candidate
command_preview_candidate
app_apply_request_candidate
```

Odin may produce these. Odin may not execute app_apply_request_candidate.

## Review Rule

High-impact candidates require one of:

- explicit app confirmation,
- explicit user confirmation,
- app-defined review flow,
- rejection/block.

## Apply Gate Contract

The app-owned Apply Gate must receive:

- candidate id,
- candidate DNA,
- why trace,
- semantic diff,
- blocked claims,
- review status.

## Red Lines

- No silent apply.
- No external send by Odin.
- No app database mutation by Odin.
- No model-to-tool shortcut.
- No semantic bus mutation event.


## Detailed Review Flow

1. Odin returns a Response Packet.
2. The app renders the candidate.
3. The app displays any high-risk status chips.
4. The app may request user or domain-owner confirmation.
5. The app apply gate receives candidate id, Candidate DNA, Why Trace, semantic diff and blocked claims.
6. The app decides whether to reject, edit, apply, send, export or defer.
7. Odin may record the app decision as feedback if the caller manifest permits derived work memory.

## High Impact Candidate Classes

High-impact candidates include:

- patchplan candidates,
- command preview candidates,
- workflow state transition candidates,
- legal or policy boundary candidates,
- app apply request candidates,
- external communication draft candidates.

Each high-impact candidate must preserve review visibility.

## Human Review Red Lines

- The review UI may not hide that the output is a candidate.
- The app may not ask Odin to silently apply.
- The app may not route direct external sending through Odin.
- The model may not decide that review is unnecessary.
- A generated runtime pack may not lower review level for high-risk actions.

## Relation to AI-Git Safety

Human review is the pull-request review analogue. The candidate is the proposed change. The semantic diff explains what changed. The Why Trace explains why the route was selected. The app apply gate is the merge button. Odin cannot press that button.
