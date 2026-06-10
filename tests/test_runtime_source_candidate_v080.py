from pathlib import Path
import json
import pytest

from odin.runtime.engine import run_universal_work_file, OdinRuntime
from odin.runtime.errors import OdinValidationError
from odin.seeds.compiler import compile_seed_pack
from odin.patterns.intake import compile_pattern_mine
from odin.work_atoms.runtime import plan_work_atoms, execute_work_atoms
from odin.hub.static_hub import build_hub_snapshot, write_static_hub
from odin.diagnostics.support_bundle import emit_support_bundle
from odin.recovery.safe_mode import build_safe_mode_plan

ROOT = Path(__file__).resolve().parents[1]


def test_full_master_architecture_runtime_flow_generates_candidate():
    result = run_universal_work_file(
        ROOT / 'examples/runtime/universal_work_full.valid.json',
        seed_pack_path=ROOT / 'examples/runtime/app_seed_pack_full.valid.json',
        pattern_mine_path=ROOT / 'examples/runtime/pattern_mine_full.valid.json',
        caller_manifest_path=ROOT / 'examples/runtime/app_caller_manifest.valid.json',
    )
    assert result['artifact_kind'] == 'odin_response_packet'
    assert result['runtime_status'] == 'candidate_generated'
    assert result['selected_candidate_id']
    candidate = result['candidates'][0]
    assert candidate['candidate_only'] is True
    assert candidate['app_owned_apply'] is True
    assert candidate['may_apply'] is False
    assert result['qirc_digest']['event_count'] >= 7
    assert result['why_trace']['steps']


def test_invalid_apply_work_is_blocked():
    work = json.loads((ROOT / 'examples/runtime/universal_work_apply_block.invalid.json').read_text(encoding='utf-8'))
    with pytest.raises(OdinValidationError):
        OdinRuntime().run_universal_work(work)


def test_seed_and_pattern_compilers_are_executable_candidates():
    seed_pack = json.loads((ROOT / 'examples/runtime/app_seed_pack_full.valid.json').read_text(encoding='utf-8'))
    compiled_seed = compile_seed_pack(seed_pack)
    assert compiled_seed['status'] == 'compiled_candidate'
    assert compiled_seed['active_seeds']
    mine = json.loads((ROOT / 'examples/runtime/pattern_mine_full.valid.json').read_text(encoding='utf-8'))
    compiled_mine = compile_pattern_mine(mine)
    assert compiled_mine['status'] == 'compiled_candidate'
    assert compiled_mine['pattern_spine']['pattern_count'] == 2


def test_work_atom_runtime_executes_micro_ops():
    work = json.loads((ROOT / 'examples/runtime/universal_work_full.valid.json').read_text(encoding='utf-8'))
    plan = plan_work_atoms(work)
    execution = execute_work_atoms(plan, {'context': {'x': 1}, 'claims': ['candidate_only'], 'actions': [], 'seeds': [], 'patterns': [], 'tags': []})
    assert execution['artifact_kind'] == 'odin_work_atom_execution'
    assert len(execution['results']) >= 5


def test_hub_support_bundle_and_safe_mode_candidates(tmp_path):
    hub_path = write_static_hub(tmp_path / 'hub' / 'index.html', build_hub_snapshot())
    assert hub_path.exists()
    bundle = emit_support_bundle(ROOT, tmp_path / 'support')
    assert bundle.exists()
    safe = build_safe_mode_plan('test')
    assert safe['artifact_kind'] == 'odin_safe_mode_plan'
    assert 'disable_remote_workers' in safe['actions']
