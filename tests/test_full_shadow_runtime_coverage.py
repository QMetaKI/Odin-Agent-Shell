import json
from pathlib import Path

from odin import cli
from odin.shadow_runtime import (
    build_shadow_context_distillation_plan,
    build_shadow_worklet_plan,
    build_shadow_gaptext,
    run_shadow_candidate_tournament,
    build_low_memory_shadow_plan,
    build_shadow_thor_bridge_plan,
    build_shadow_bounded_code_plan,
    build_shadow_trace_record,
    build_shadow_api_plan,
    validate_shadow_app_qirc_digest,
    score_shadow_model_dojo,
    redact_shadow_payload,
    build_shadow_support_bundle_manifest,
    build_shadow_windows_runtime_plan,
    validate_shadow_sdk_template,
)

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT / 'examples' / 'shadow_runtime' / name).read_text(encoding='utf-8'))

def test_validate_full_shadow_runtime_coverage_clean():
    assert cli.validate_shadow_runtime() == []

def test_artifact_lens_context_and_worklet_gaptext_shadow():
    work = load('artifact_lens_context_shadow.valid.json')
    plan = build_shadow_context_distillation_plan(work)
    assert 'wedding_speech_lens' in plan['active_lenses']
    wplan = build_shadow_worklet_plan(work)
    assert wplan['claim_boundary'].endswith('candidate_only')
    gap = build_shadow_gaptext(work)
    assert 'verified_claim' in gap['sections']['forbidden']

def test_candidate_tournament_and_low_memory_shadow():
    tournament = run_shadow_candidate_tournament(load('candidate_tournament_shadow.valid.json'), load('candidate_tournament_shadow.valid.json')['candidates'])
    assert tournament['selected_candidate_id'] == 'B'
    low = build_low_memory_shadow_plan(load('low_memory_shadow.valid.json'))
    assert 'normal_7b_route' in low['disabled_features']

def test_thor_bounded_code_storage_api_shadow():
    thor = build_shadow_thor_bridge_plan(load('thor_bridge_shadow.valid.json'))
    assert thor['return_contract']['candidate_only'] is True
    code = build_shadow_bounded_code_plan(load('bounded_code_shadow.valid.json'))
    assert 'patch_applied' in code['forbidden_claims']
    trace = build_shadow_trace_record(load('storage_trace_shadow.valid.json'))
    assert trace['receipt_candidate']['external_verification'] is False
    api = build_shadow_api_plan(load('api_shadow.valid.json')['endpoint'], load('api_shadow.valid.json'))
    assert api['localhost_only'] is True

def test_app_qirc_model_dojo_security_support_windows_sdk_shadow():
    ok = validate_shadow_app_qirc_digest(load('app_qirc_bridge_shadow.valid.json'))
    assert ok['ok'] is True and ok['odin_owns_app_qirc'] is False
    bad = validate_shadow_app_qirc_digest(load('app_qirc_bridge_blocked.invalid.json'))
    assert bad['ok'] is False
    dojo = score_shadow_model_dojo(**load('model_dojo_shadow.valid.json'))
    assert 'json_fill' in dojo['best_for']
    red = redact_shadow_payload(load('security_redaction_shadow.valid.json')['payload'])
    assert red['secret_hits'] >= 1 and red['remote_allowed'] is False
    support = build_shadow_support_bundle_manifest(load('support_bundle_shadow.valid.json')['work_id'])
    assert support['redaction_required'] is True
    windows = build_shadow_windows_runtime_plan(load('windows_runtime_shadow.valid.json')['mode'])
    assert 'odin-daemon' in windows['processes']
    sdk = validate_shadow_sdk_template(**load('sdk_template_shadow.valid.json'))
    assert sdk['ok'] is True

def test_pr24_and_real_pr10_registered():
    tasks = json.loads((ROOT / 'registries' / 'codex_task_registry.json').read_text())['tasks']
    assert any(task['id'] == 'PR-24' for task in tasks)
    bundles = json.loads((ROOT / 'registries' / 'codex_pr_bundle_registry.json').read_text())['bundles']
    assert any(bundle['id'] == 'REAL-PR-10' and 'PR-24' in bundle['internal_tasks'] for bundle in bundles)
