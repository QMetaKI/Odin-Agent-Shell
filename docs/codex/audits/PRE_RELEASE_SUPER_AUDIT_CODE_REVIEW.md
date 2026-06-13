
# PRE-RELEASE SUPER AUDIT — Code Review Simulation

| Checklist item | Result |
| --- | --- |
| audit script stdlib-only or existing deps | stdlib-only plus existing Odin imports |
| subprocess usage restricted to local deterministic commands | yes |
| no public network calls | yes, localhost-only endpoint smoke |
| no provider/model calls | yes |
| no API keys | yes |
| reports deterministic enough | yes, stable timestamps and sorted JSON |
| JSON outputs parse | covered by tests |
| Markdown outputs present | covered by tests |
| tests deterministic | yes, lightweight mode exists |
| CLI command works | `audit-pre-release-super` added |
| FILE_MANIFEST complete | updated after file generation |
| SYSTEM_MAP complete | pre_release_super_audit entry added |
| validate-all not made too heavy | audit command not integrated into validate-all |
| full pytest result recorded | runtime report records full pytest when non-lightweight audit runs |

Applied fix from review: test mode uses `--lightweight` to avoid recursive full-suite execution.
