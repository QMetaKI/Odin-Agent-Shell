import json
from pathlib import Path

from odin.cli import validate_real_pr_execution

ROOT = Path(__file__).resolve().parents[1]


def test_build_ladder_is_absolutely_aligned():
    assert validate_real_pr_execution() == []
    data = json.loads((ROOT / 'registries/real_pr_execution_registry.json').read_text(encoding='utf-8'))
    assert data['alignment_lock'] == 'BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK'
    assert len(data['execution_prs']) == 8


def test_internal_tasks_are_mapped_exactly_once():
    data = json.loads((ROOT / 'registries/real_pr_execution_registry.json').read_text(encoding='utf-8'))
    task_registry = json.loads((ROOT / 'registries/codex_task_registry.json').read_text(encoding='utf-8'))
    task_ids = {task['id'] for task in task_registry['tasks']}
    mapped = [tid for pr in data['execution_prs'] for tid in pr['absorbs_internal_tasks']]
    assert set(mapped) == task_ids
    assert len(mapped) == len(set(mapped))


def test_legacy_bundles_are_absorbed_at_least_once():
    data = json.loads((ROOT / 'registries/real_pr_execution_registry.json').read_text(encoding='utf-8'))
    bundle_registry = json.loads((ROOT / 'registries/codex_pr_bundle_registry.json').read_text(encoding='utf-8'))
    bundle_ids = {bundle['id'] for bundle in bundle_registry['bundles']}
    absorbed = {bid for pr in data['execution_prs'] for bid in pr['absorbs_legacy_bundles']}
    assert bundle_ids <= absorbed


def test_existing_and_target_paths_are_separated():
    data = json.loads((ROOT / 'registries/real_pr_execution_registry.json').read_text(encoding='utf-8'))
    for pr in data['execution_prs']:
        for rel in pr['expected_existing_paths']:
            assert (ROOT / rel).exists(), (pr['id'], rel)
        assert set(pr['existing_files']) == set(pr['expected_existing_paths'])
        assert set(pr['target_files']) == set(pr['expected_new_paths'])
        assert pr['acceptance_gates']
        assert pr['proof_boundaries']
        assert pr['master_architecture_sections']
