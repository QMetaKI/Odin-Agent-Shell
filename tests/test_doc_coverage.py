from pathlib import Path
from odin.cli import validate_docs

ROOT = Path(__file__).resolve().parents[1]

def test_full_docs_expansion_coverage():
    assert validate_docs() == []


def test_master_docs_are_substantial():
    arch = (ROOT / "docs/MASTER_ARCHITECTURE_V7_1.md").read_text(encoding="utf-8")
    specs = (ROOT / "docs/MASTER_SPECS_V7_1.md").read_text(encoding="utf-8")
    assert "Internal Semantic IRC Bus" in arch
    assert "Model Scale Ladder" in arch
    assert "Repository Layout Spec" in specs
    assert "ModelWorkPacket" in specs
    assert len(arch) > 80000
    assert len(specs) > 80000
    assert "App QIRC Bridge" in arch
    assert "Provider Adapter Spec" in specs
    assert "Semantic Event Envelope" in arch
