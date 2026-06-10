from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json

from odin.runtime.errors import OdinValidationError


@dataclass(frozen=True)
class OdinRuntimeConfig:
    protocol_version: str = "7.1"
    runtime_candidate_version: str = "0.8.6"
    runtime_dir: str = ".odin_runtime"
    host_scope: str = "local_dev_candidate"
    remote_workers_enabled: bool = False
    app_apply_owned: bool = True
    qirc_network_enabled: bool = False
    model_inference_required: bool = False
    config_source: str = "defaults"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["claim_boundary"] = "runtime_config_is_local_candidate_configuration_not_host_proof"
        return data


_ALLOWED_FIELDS = set(OdinRuntimeConfig.__dataclass_fields__)


def _read_config_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise OdinValidationError(
            f"invalid runtime config JSON at {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def load_runtime_config(path: str | Path | None = None, *, strict: bool = False) -> OdinRuntimeConfig:
    """Load local runtime candidate configuration.

    Missing optional config files resolve to deterministic defaults unless
    ``strict=True`` is requested. Present malformed files always raise a bounded
    validation error. This loader performs no network, process, provider, or app
    state side effects.
    """
    if path is None:
        return OdinRuntimeConfig(config_source="defaults")
    p = Path(path)
    if not p.exists():
        if strict:
            raise OdinValidationError(f"runtime config file not found: {p}")
        return OdinRuntimeConfig(config_source=f"defaults_missing_optional:{p}")
    data = _read_config_json(p)
    if not isinstance(data, dict):
        raise OdinValidationError(f"runtime config must be a JSON object: {p}")
    unknown = sorted(set(data) - _ALLOWED_FIELDS)
    clean = {k: v for k, v in data.items() if k in _ALLOWED_FIELDS}
    clean["config_source"] = str(p)
    cfg = OdinRuntimeConfig(**clean)
    if unknown:
        # Unknown config fields are intentionally ignored for compatibility, but
        # their presence is made visible to callers without changing authority.
        object.__setattr__(cfg, "config_source", f"{p} ignored_unknown={','.join(unknown)}")
    return cfg
