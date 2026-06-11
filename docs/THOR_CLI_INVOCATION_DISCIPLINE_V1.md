# Thor CLI Invocation Discipline V1

**Claim boundary:** `thor_cli_invocation_discipline_doc_candidate_only_advisory`

**Version:** 1.0
**Added:** LRH-PR-13

---

## Purpose

This document defines the Thor CLI invocation discipline for Odin Agent Shell workers.

It ensures future workers know exactly how to discover, invoke, reinstall, classify, and report Thor — and do not write vague "Thor unavailable" without diagnostics.

---

## Thor's Role

**Thor is advisory only.**

Odin repo validators (`python -m odin.cli validate-all`) and pytest remain the authority.

Thor failure does not automatically block feature PRs, but the failure **must be diagnosed precisely** using the classification below.

Do not write "Thor unavailable" without PATH/module/install/clone diagnostics.

---

## Expected Thor Availability

Thor is available as a CLI tool installed from the Thor-Agent-Kit repository:
- Repo: `https://github.com/QMetaKI/Thor-Agent-Kit.git`
- Install path: `/tmp/thor-agent-kit` (recommended clone target for workers)
- Entry point: `thor` (added to PATH after pip install)

Thor is **not** a dependency of `odin-agent-shell`. It is a separate advisory toolchain.
Workers should expect to install it fresh per session if not present.

---

## Preferred Invocation Order

1. Check if `thor` is in PATH: `command -v thor`
2. If not found, check `/tmp/thor-agent-kit`: `[ -d /tmp/thor-agent-kit ]`
3. If found, install from `/tmp/thor-agent-kit`: `pip install -e ".[dev]"`
4. If not found, clone and install:
   ```bash
   git clone --depth=1 https://github.com/QMetaKI/Thor-Agent-Kit.git /tmp/thor-agent-kit
   cd /tmp/thor-agent-kit && pip install -e ".[dev]"
   ```
5. Return to Odin repo: `cd <odin-repo-root>`
6. Verify: `command -v thor && thor --help`

---

## PATH Check

```bash
echo "$PATH"
command -v thor || echo "thor: not in PATH"
which thor 2>/dev/null || echo "which thor: not found"
```

If not found after install, check:
```bash
echo "$PATH"
ls /root/.local/bin/ | grep thor
ls /usr/local/bin/ | grep thor
```

---

## Python Module Check

```bash
python - <<'PY'
import sys, importlib.util
for m in ["thor", "thor_agent_kit", "thor_agent", "thor_agent_kit.cli"]:
    print(m, importlib.util.find_spec(m))
print("python", sys.executable)
PY
```

Module availability does not guarantee CLI availability. Check both.

---

## /tmp/thor-agent-kit Reuse

If `/tmp/thor-agent-kit` exists from a prior session:
```bash
if [ -d /tmp/thor-agent-kit ]; then
  cd /tmp/thor-agent-kit
  python -m pip install -e ".[dev]" -q
  cd <odin-repo-root>
fi
```

Do not delete `/tmp/thor-agent-kit` unless it is corrupt.

---

## Fresh Clone / Install Fallback

If `/tmp/thor-agent-kit` does not exist:
```bash
git clone --depth=1 https://github.com/QMetaKI/Thor-Agent-Kit.git /tmp/thor-agent-kit
cd /tmp/thor-agent-kit
python -m pip install -e ".[dev]"
cd <odin-repo-root>
```

Network is required for fresh clone. If network is unavailable, classify as `network_unavailable`.

---

## Working Directory Discipline

**Always return to the Odin repo root before running `thor` commands.**

Thor session state is stored under `.thor/` relative to cwd. If cwd is wrong:
- `thor doctor` may fail with missing schema/agent files (those belong to Thor's own repo)
- `thor map` may produce wrong repo map
- `thor start` may create session in wrong directory

```bash
cd /home/user/Odin-Agent-Shell  # or your Odin repo root
thor start "task description"
thor map
```

**Do not run `thor doctor` from `/tmp/thor-agent-kit`** — Thor's own repo lacks the schema files that `doctor` checks for. Run from the Odin repo.

---

## Known Command Set

| Command | Purpose |
|---------|---------|
| `thor doctor` | Health check (run from Odin repo, not Thor repo) |
| `thor validate` | Validate Thor's own files (run from Thor repo; usually 0 items to check) |
| `thor start "task"` | Create new Thor session |
| `thor map` | Write repo map to `.thor/repo/repo_map.json` |
| `thor plan` | Generate task plan (requires active session) |
| `thor guard` | Write guard model for protected surfaces |
| `thor expected` | Write expected output contract |
| `thor handoff --depth full` | Render full handoff packet |
| `thor pack --agent claude-code` | Write agent-specific handoff pack |
| `thor repo cognition --profile max` | Repo cognition analysis |
| `thor repo intent "task"` | Derive repo intent for task |
| `thor y analyze "task"` | Y-flow task analysis |
| `thor y handoff-spine "task"` | Y-flow handoff spine |

---

## Diagnostic Commands

Run and save diagnostics before reporting failure:

```bash
{
  echo "# Thor Diagnostic"
  echo "cwd: $(pwd)"
  echo "PATH: $PATH"
  command -v thor || echo "thor: not in PATH"
  python -m pip show thor-agent-kit 2>/dev/null || echo "pip show: not found"
  find . -maxdepth 4 -iname '*thor*' -print 2>/dev/null | head -10
  find /tmp -maxdepth 4 -iname '*thor*' -print 2>/dev/null | head -5
} > /tmp/odin-thor-summaries/THOR_DIAGNOSTIC.md
```

---

## Classification of Failure Modes

Workers must classify Thor unavailability as one of:

| Class | Description |
|-------|-------------|
| `thor_available` | Thor installed, in PATH, responds to commands |
| `not_found_in_PATH` | `thor` binary not in PATH; may still be installable |
| `entrypoint_missing_after_install` | pip install succeeded but `thor` not in PATH |
| `module_not_importable_after_install` | pip install succeeded but import fails |
| `clone_unavailable` | git clone of Thor-Agent-Kit failed |
| `network_unavailable` | No network access for fresh clone |
| `permission_issue` | pip install blocked by permissions |
| `working_directory_issue` | cwd wrong — run from Odin repo root |
| `unknown_invocation_regression` | None of the above; capture full diagnostic output |

**Do not write "Thor unavailable" without recording one of these classifications.**

---

## Blocking vs Non-Blocking

Thor failure is **non-blocking** for feature PRs when:
- All Odin validators pass (`python -m odin.cli validate-all`)
- All pytest tests pass
- Failure is diagnosed and classified

Thor failure is **blocking** only if:
- The PR's explicit acceptance gate requires Thor output as authority (rare)
- The failure indicates a repo problem (wrong cwd, missing Odin files)

---

## Thor Summary Artifact Pattern

Every PR that runs Thor must produce:

`/tmp/odin-thor-summaries/<PR-ID>_THOR_SUMMARY.md`

Required sections:
- `## Diagnostic` — classification, PATH, module, clone status
- `## Commands` — list each command run and its output summary
- `## Effect on Implementation` — boundaries reinforced, allowed files, forbidden scope
- `## Boundary` — "Thor is advisory only. Odin repo validators and tests remain authority."

Do not commit `/tmp/odin-thor-summaries/` to the repo.

---

## How to Cite Thor Output in Return Reports

In `docs/codex/reports/LRH-PR-NN_RETURN_REPORT.md`:

```
## Thor Diagnostic and Invocation Discipline

Classification: thor_available | not_found_in_PATH | ...
Install: [how thor was installed / what was attempted]
Commands run: doctor, validate, start, map, guard, expected, handoff, pack
Key outputs: [brief summaries]
Advisory use: [boundaries reinforced, scope confirmed]

Thor is advisory only. Odin validators remain authority.
PR result does not depend on Thor output.
```

---

## What Not to Claim

- Do not claim Thor verified correctness of Odin code
- Do not claim Thor output as proof of production readiness
- Do not claim Thor validated Odin security
- Do not state "Thor passed" as a proof boundary
- Do not state "Thor unavailable" without classification
- Do not let Thor failure silently drop without diagnosis
