REQUIRED_EVENT_FIELDS = {
    "artifact_kind","protocol_version","event_id","channel","event_type",
    "source_module","trace_id","privacy_class","payload","created_at"
}

def validate_semantic_event(event: dict) -> list[str]:
    errors = []
    missing = REQUIRED_EVENT_FIELDS - set(event)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if event.get("artifact_kind") != "odin_semantic_event":
        errors.append("artifact_kind must be odin_semantic_event")
    if not str(event.get("channel","")).startswith("#"):
        errors.append("channel must start with #")
    if event.get("privacy_class") == "blocked_sensitive":
        errors.append("blocked_sensitive events may not be published to bus")
    return errors
