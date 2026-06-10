import json
from pathlib import Path
from odin.semantic_bus.event_envelope import validate_semantic_event

def test_valid_semantic_event():
    data = json.loads(Path("examples/semantic_bus/context_capsule_event.valid.json").read_text())
    assert validate_semantic_event(data) == []

def test_rejects_non_channel():
    data = json.loads(Path("examples/semantic_bus/context_capsule_event.valid.json").read_text())
    data["channel"] = "context.distill"
    assert "channel must start with #" in validate_semantic_event(data)
