"""Runtime security smoke validator — FINAL-PR-04.

Claim boundary: runtime_security_smoke_not_security_certification
candidate_only: true
local_only: true

Checks runtime boundaries without executing providers or reading secrets.
This is a smoke check, NOT a security certification or audit.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

CLAIM_BOUNDARY = "runtime_security_smoke_not_security_certification"

# Forbidden markers — scanned in provider and security source files only
FORBIDDEN_MARKERS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "os.environ.get(\"OPENAI",
    "os.environ.get(\"ANTHROPIC",
    "os.getenv(\"OPENAI",
    "os.getenv(\"ANTHROPIC",
    "ollama run",
    "ollama generate",
    "ollama chat",
    "ollama embed",
    "allow_public_network=True",
    "allow_federation=True",
    "0.0.0.0",
]

# Patterns that indicate potential external network calls (scanned in provider/security files)
EXTERNAL_NETWORK_PATTERNS = [
    r'requests\.get\(',
    r'requests\.post\(',
    r'httpx\.',
]

# Files/dirs to scan for forbidden markers (relative to repo root)
SCAN_DIRS = [
    "odin/providers",
    "odin/runtime_security",
    "odin/execution_gate",
]

# Files exempt from scanning: scanner itself (defines marker strings as data),
# and server.py which uses urllib for localhost-only connections.
SCAN_EXCEPTION_FILES = {
    "odin/runtime_security/smoke.py",  # this file defines markers as data constants
    "odin/local_hub/server.py",       # uses urllib for local smoke test
}


@dataclass
class RuntimeSecuritySmokeResult:
    status: str = "ok"
    forbidden_findings: list[dict] = field(default_factory=list)
    provider_execution_default: bool = False
    model_inference_default: bool = False
    api_key_reads: bool = False
    external_network: bool = False
    public_bind: bool = False
    candidate_only: bool = True
    local_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def as_dict(self) -> dict:
        return {
            "artifact_kind": "odin_runtime_security_smoke_result",
            "status": self.status,
            "candidate_only": self.candidate_only,
            "local_only": self.local_only,
            "forbidden_findings": self.forbidden_findings,
            "provider_execution_default": self.provider_execution_default,
            "model_inference_default": self.model_inference_default,
            "api_key_reads": self.api_key_reads,
            "external_network": self.external_network,
            "public_bind": self.public_bind,
            "claim_boundary": self.claim_boundary,
        }


def _scan_content_for_forbidden(content: str, source: str) -> list[dict]:
    findings = []
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for marker in FORBIDDEN_MARKERS:
            if marker in line:
                findings.append({
                    "source": source,
                    "line": i,
                    "marker": marker,
                    "excerpt": line.strip()[:120],
                })
        for pattern in EXTERNAL_NETWORK_PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "source": source,
                    "line": i,
                    "marker": pattern,
                    "excerpt": line.strip()[:120],
                })
    return findings


def _scan_file(path: Path, repo_root: Path) -> list[dict]:
    rel = str(path.relative_to(repo_root))
    if rel in SCAN_EXCEPTION_FILES:
        return []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    return _scan_content_for_forbidden(content, rel)


def _scan_repo(repo_root: Path) -> list[dict]:
    findings = []
    for scan_dir in SCAN_DIRS:
        d = repo_root / scan_dir
        if not d.exists():
            continue
        for path in sorted(d.rglob("*.py")):
            findings.extend(_scan_file(path, repo_root))
    return findings


def _check_provider_policy_boundaries() -> list[dict]:
    from odin.providers.registry import PROVIDER_REGISTRY
    findings = []
    for pid, entry in PROVIDER_REGISTRY.items():
        if entry.get("execution_allowed", False):
            findings.append({
                "source": "provider_registry",
                "provider_id": pid,
                "marker": "execution_allowed=True",
                "excerpt": f"provider {pid} has execution_allowed=True",
            })
        if entry.get("requires_api_key", False):
            findings.append({
                "source": "provider_registry",
                "provider_id": pid,
                "marker": "requires_api_key=True",
                "excerpt": f"provider {pid} has requires_api_key=True",
            })
        if entry.get("remote", False):
            findings.append({
                "source": "provider_registry",
                "provider_id": pid,
                "marker": "remote=True",
                "excerpt": f"provider {pid} has remote=True",
            })
    return findings


def _check_execution_gate_policy_boundaries() -> list[dict]:
    """Verify execution gate policy does not enable forbidden execution by default."""
    findings = []
    try:
        from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY as p
        if p.local_candidate_execution_allowed:
            findings.append({
                "source": "execution_gate_policy",
                "marker": "local_candidate_execution_allowed=True",
                "excerpt": "DEFAULT_EXECUTION_GATE_POLICY has local_candidate_execution_allowed=True",
            })
        if p.remote_execution_allowed:
            findings.append({
                "source": "execution_gate_policy",
                "marker": "remote_execution_allowed=True",
                "excerpt": "DEFAULT_EXECUTION_GATE_POLICY has remote_execution_allowed=True",
            })
        if p.api_key_reads_allowed:
            findings.append({
                "source": "execution_gate_policy",
                "marker": "api_key_reads_allowed=True",
                "excerpt": "DEFAULT_EXECUTION_GATE_POLICY has api_key_reads_allowed=True",
            })
        if p.external_network_allowed:
            findings.append({
                "source": "execution_gate_policy",
                "marker": "external_network_allowed=True",
                "excerpt": "DEFAULT_EXECUTION_GATE_POLICY has external_network_allowed=True",
            })
        if p.app_apply_allowed:
            findings.append({
                "source": "execution_gate_policy",
                "marker": "app_apply_allowed=True",
                "excerpt": "DEFAULT_EXECUTION_GATE_POLICY has app_apply_allowed=True",
            })
        if p.external_send_allowed:
            findings.append({
                "source": "execution_gate_policy",
                "marker": "external_send_allowed=True",
                "excerpt": "DEFAULT_EXECUTION_GATE_POLICY has external_send_allowed=True",
            })
    except Exception as exc:
        findings.append({
            "source": "execution_gate_policy",
            "marker": "import_error",
            "excerpt": str(exc)[:120],
        })
    return findings


def scan_content(content: str, source: str = "synthetic") -> list[dict]:
    """Public API: scan arbitrary content for forbidden markers. Used in tests."""
    return _scan_content_for_forbidden(content, source)


def run_runtime_security_smoke(repo_root: Path | None = None) -> RuntimeSecuritySmokeResult:
    if repo_root is None:
        repo_root = Path(__file__).resolve().parents[2]

    result = RuntimeSecuritySmokeResult()
    all_findings: list[dict] = []

    # 1. Static scan of provider/security source files
    file_findings = _scan_repo(repo_root)
    all_findings.extend(file_findings)

    # 2. Policy boundary check — all providers must have execution_allowed=False
    policy_findings = _check_provider_policy_boundaries()
    all_findings.extend(policy_findings)

    # 3. Execution gate policy boundary check — FINAL-PR-05
    gate_findings = _check_execution_gate_policy_boundaries()
    all_findings.extend(gate_findings)

    result.forbidden_findings = all_findings
    result.api_key_reads = any(
        m in f.get("marker", "")
        for f in all_findings
        for m in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY")
    )
    result.external_network = any(
        any(m in f.get("marker", "") for m in ("requests.get", "requests.post", "httpx."))
        for f in all_findings
    )
    result.public_bind = any("0.0.0.0" in f.get("marker", "") for f in all_findings)
    result.provider_execution_default = False
    result.model_inference_default = False

    if all_findings:
        result.status = "findings"
    else:
        result.status = "ok"

    return result
