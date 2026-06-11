"""Audit artifact checks for the post LRH-PR-18 full-system audit.

Claim boundary: audit_artifact_structure_check_not_runtime_or_release_proof
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "rebaseline" / "FULL_SYSTEM_AUDIT_AFTER_LRH_PR_18.md"


def _text() -> str:
    return AUDIT.read_text(encoding="utf-8")


def test_full_system_audit_after_lrh_pr_18_exists():
    assert AUDIT.exists()


def test_full_system_audit_has_required_stable_sections():
    text = _text()
    required_sections = [
        "## 0. Claim Boundary",
        "## 1. Machine-Readable Audit Summary",
        "## 4. Evidence Ledger",
        "## 8. Capability Matrix",
        "## 26. Risk Register",
        "## 27. Gap Register",
        "## 32. Final Verdict",
        "## 36. Appendix D — Future ChatGPT Intake Order",
    ]
    for section in required_sections:
        assert section in text


def test_full_system_audit_preserves_non_claim_boundaries():
    text = _text()
    required_phrases = [
        "kein Produktions-",
        "signed distribution",
        "Windows service/tray/installer proof",
        "target-host validation",
        "live model inference",
        "specific external app integration",
        "external_receipt_required",
        "retained_gap",
        "non_goal_boundary",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_full_system_audit_has_machine_readable_ids():
    text = _text()
    for stable_id in ["E001", "F001", "C001", "L001", "R001", "G001", "A001", "X001"]:
        assert stable_id in text
