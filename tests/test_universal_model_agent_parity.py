from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_universal_model_agent_docs_exist():
    docs = [
        'docs/UNIVERSAL_MODEL_AGENT_PARITY_V7_1.md',
        'docs/MODEL_AGENT_CAPABILITY_CARDS_V7_1.md',
        'docs/MODEL_AGENT_WORK_CAPSULES_V7_1.md',
        'docs/UNIVERSAL_AGENT_CANDIDATE_PROTOCOL_V7_1.md',
        'docs/MODEL_AGENT_PERMISSION_CARD_SYSTEM_V7_1.md',
        'docs/EXTERNAL_MODEL_AGENT_ADAPTER_BOUNDARY_V7_1.md',
        'docs/UNIVERSAL_AGENT_ORCHESTRATION_MATRIX_V7_1.md',
        'docs/MODEL_AGENT_WHY_TRACE_V7_1.md',
        'docs/UNIVERSAL_MODEL_AGENT_PARITY_CONSOLIDATION_V7_1.md',
    ]
    for rel in docs:
        text = (ROOT / rel).read_text(encoding='utf-8')
        assert 'candidate' in text.lower()
        assert 'No model or agent' in text or 'No model' in text


def test_model_agent_registries_valid():
    for rel in [
        'registries/model_agent_card_registry.json',
        'registries/model_agent_adapter_registry.json',
        'registries/model_agent_permission_registry.json',
        'registries/universal_agent_parity_registry.json',
        'registries/agent_candidate_protocol_registry.json',
        'registries/agent_twin_archetype_registry.json',
    ]:
        data = json.loads((ROOT / rel).read_text(encoding='utf-8'))
        assert data['registry_id']
        assert data['version'] == '0.6.6'


def test_codex_tasks_and_bundle_cover_universal_agent_parity():
    tasks = json.loads((ROOT / 'registries/codex_task_registry.json').read_text(encoding='utf-8'))['tasks']
    task_ids = {task['id'] for task in tasks}
    for i in range(66, 73):
        assert f'PR-{i:02d}' in task_ids
    bundles = json.loads((ROOT / 'registries/codex_pr_bundle_registry.json').read_text(encoding='utf-8'))['bundles']
    bundle = next(b for b in bundles if b['id'] == 'REAL-PR-19')
    assert bundle['internal_tasks'] == [f'PR-{i:02d}' for i in range(66, 73)]


def test_shadow_modules_present():
    for rel in [
        'odin/shadow_runtime/universal_model_agent_parity_shadow.py',
        'odin/shadow_runtime/model_agent_card_shadow.py',
        'odin/shadow_runtime/agent_work_capsule_shadow.py',
        'odin/shadow_runtime/agent_capability_pack_shadow.py',
        'odin/shadow_runtime/external_agent_adapter_shadow.py',
        'odin/shadow_runtime/agent_permission_card_shadow.py',
        'odin/shadow_runtime/agent_candidate_protocol_shadow.py',
        'odin/shadow_runtime/agent_twin_archetype_shadow.py',
        'odin/shadow_runtime/universal_agent_why_trace_shadow.py',
    ]:
        assert (ROOT / rel).exists()
