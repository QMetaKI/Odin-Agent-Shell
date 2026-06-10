# Universal Use Case Matrix v7.1

## Purpose
The Universal Use Case Matrix defines how arbitrary LLM and agent use cases map to Odin work profiles.

## Matrix
| Use case | Preferred worker | Odin layer | Output |
|---|---|---|---|
| JSON / schema repair | 3B or deterministic | Slot Forge + Schema Gate | json_candidate |
| Intent routing | 3B | QIRC + Seed Economy | route_candidate |
| Document summary | 7B or hybrid | Hot Window + Context Distillery | summary_candidate |
| Code review | hybrid or coding agent | Thor + Semantic Diff | review_candidate |
| Patch planning | hybrid / coding agent | Thor Handoff Compiler | patchplan_candidate |
| Research | remote/local research worker | Adapter + Evidence Gate | research_candidate |
| App workflow | hybrid | Work Capsule + Permission Card | action_card_candidate |
| Game NPC/Quest | hybrid | State Lens + Role Seeds | dialogue_candidate |
| Ceremony/studio | hybrid | Wedding Lens + Style Seeds | document_section_candidate |
| Low-memory helper | 1B/2B/3B | Low Memory Strict Pack | micro_candidate |

## Principle
Every use case has a smallest sufficient worker and a candidate output. If no safe candidate route exists, Odin asks for context, splits work, holds or blocks.


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
