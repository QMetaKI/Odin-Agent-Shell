import json
from pathlib import Path
from odin.universal_work.universal_work_validator import validate_universal_work

def test_valid_universal_work():
    data = json.loads(Path("examples/universal_work/rewrite_markdown.valid.json").read_text())
    assert validate_universal_work(data) == []

def test_rejects_non_candidate_output():
    data = json.loads(Path("examples/universal_work/rewrite_markdown.valid.json").read_text())
    data["output_contract"]["candidate_only"] = False
    assert "output_contract.candidate_only must be true" in validate_universal_work(data)
