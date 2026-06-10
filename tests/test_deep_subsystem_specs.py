from pathlib import Path
from odin.cli import validate_docs

ROOT = Path(__file__).resolve().parents[1]

def test_deep_subsystem_doc_validation_clean():
    assert validate_docs() == []

def test_deep_subsystem_docs_have_real_weight():
    required = {
        "docs/DATA_CONTRACTS_V7_1.md": 12000,
        "docs/ALGORITHMS_V7_1.md": 12000,
        "docs/IMPLEMENTATION_DOD_V7_1.md": 12000,
        "docs/UNIVERSAL_WORK_KERNEL.md": 12000,
        "docs/SMALL_MODEL_POWER_LAYER.md": 11000,
        "docs/INTERNAL_SEMANTIC_BUS.md": 10000,
    }
    for rel, minimum in required.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert len(text) >= minimum, rel
        assert "v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK" in text or "Deep Subsystem Spec" in text
