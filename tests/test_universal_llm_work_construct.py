from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]


def test_universal_llm_docs_exist():
    required = [
        "docs/UNIVERSAL_LLM_WORK_CONSTRUCT_V7_1.md",
        "docs/THOR_ODIN_AI_GIT_LAYER_V7_1.md",
        "docs/UNIVERSAL_MODEL_AGENT_ADAPTERS_V7_1.md",
        "docs/REMOTE_MODEL_WORKER_BOUNDARY_V7_1.md",
        "docs/LOCAL_REMOTE_LLM_PARITY_V7_1.md",
        "docs/AGENT_TOOL_PERMISSION_BOUNDARY_V7_1.md",
        "docs/UNIVERSAL_USE_CASE_MATRIX_V7_1.md",
        "docs/ANY_MODEL_ANY_AGENT_SAME_BOUNDARY_V7_1.md",
    ]
    for rel in required:
        p = ROOT / rel
        assert p.exists(), rel
        text = p.read_text(encoding="utf-8")
        assert "Candidate" in text
        assert "app" in text.lower()


def test_gpl2_policy_files_exist():
    for rel in ["LICENSE", "LICENSE_POLICY.md", "THOR_ODIN_GPL2_ONLY_POLICY.md", "PROTOCOL_BOUNDARY.md", "SPDX_POLICY.md", "THIRD_PARTY_NOTICES.md"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "GPL-2.0-only" in text or rel == "THIRD_PARTY_NOTICES.md"


def test_real_pr_21_covers_tasks():
    reg = json.loads((ROOT / "registries" / "codex_pr_bundle_registry.json").read_text(encoding="utf-8"))
    bundle = next(b for b in reg["bundles"] if b["id"] == "REAL-PR-21")
    assert set(bundle["internal_tasks"]) == {f"PR-{i:02d}" for i in range(81, 87)}
