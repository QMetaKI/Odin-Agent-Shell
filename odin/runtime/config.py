from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json

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

    def to_dict(self) -> dict:
        data = asdict(self)
        data["claim_boundary"] = "runtime_config_is_local_candidate_configuration_not_host_proof"
        return data


def load_runtime_config(path: str | Path | None = None) -> OdinRuntimeConfig:
    if path is None:
        return OdinRuntimeConfig()
    p = Path(path)
    if not p.exists():
        return OdinRuntimeConfig()
    data = json.loads(p.read_text(encoding="utf-8"))
    allowed = {field.name for field in OdinRuntimeConfig.__dataclass_fields__.values()}
    clean = {k: v for k, v in data.items() if k in allowed}
    return OdinRuntimeConfig(**clean)
