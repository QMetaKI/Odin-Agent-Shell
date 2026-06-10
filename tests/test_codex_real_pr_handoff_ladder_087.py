import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_codex_handoff_registry_matches_real_execution_ladder():
    real = load("registries/real_pr_execution_registry.json")
    handoff = load("registries/codex_real_pr_handoff_registry.json")
    assert real["version"] == "0.8.7"
    assert real["codex_handoff_lock"] == "CODEX_REAL_PR_HANDOFF_LADDER_LOCK"
    assert handoff["version"] == "0.8.7"
    assert [p["id"] for p in real["execution_prs"]] == [p["id"] for p in handoff["execution_prs"]]
    assert len(real["execution_prs"]) == 8


def test_every_real_pr_has_post_runtime_candidate_fields_and_prompt():
    real = load("registries/real_pr_execution_registry.json")
    for pr in real["execution_prs"]:
        assert pr["current_base"] == "v0.8.6_DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK"
        assert pr["codex_execution_mode"] == "post_chatgpt_runtime_candidate_completion_pr"
        assert pr["chatgpt_materialized"]
        assert pr["codex_completion_focus"]
        assert pr["codex_deliverables"]
        assert pr["senior_review_focus"]
        assert pr["return_report_required"] is True
        prompt = ROOT / pr["handoff_doc"]
        assert prompt.exists(), pr["handoff_doc"]
        text = prompt.read_text(encoding="utf-8")
        for anchor in [pr["id"], "Already materialized by ChatGPT", "Codex completion focus", "Proof boundaries", "Return format"]:
            assert anchor in text


def test_codex_handoff_docs_exist_and_reference_v086_base():
    for rel in [
        "docs/CODEX_REAL_PR_HANDOFF_LADDER_LOCK_V0_8_7.md",
        "docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md",
        "docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md",
        "docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md",
        "docs/reviews/SENIOR_REVIEW_SIMULATION_V0_8_7_CODEX_REAL_PR_LADDER.md",
    ]:
        p = ROOT / rel
        assert p.exists(), rel
        text = p.read_text(encoding="utf-8")
        assert "v0.8.6" in text or "post-v0.8.6" in text
