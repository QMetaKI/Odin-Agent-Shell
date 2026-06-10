from odin.shadow_runtime.fairy_dsl_shadow import FairyStoryShadow, validate_fairy_story_shadow
from odin.shadow_runtime.ystar_native_dsl_shadow import YStarNativeUnitShadow, validate_ystar_unit_shadow
from odin.shadow_runtime.narrative_aorta_shadow import NarrativeAortaNodeShadow, validate_aorta_node_shadow
from odin.shadow_runtime.fairy_to_shadow_ir_shadow import FairyShadowMapping, lower_mapping_to_shadow_fragment
from odin.shadow_runtime.ystar_mediation_shadow import YStarMediationDirectiveShadow, validate_ystar_mediation_shadow
from odin.compiler.pack_manifest import build_pack_manifest
from odin.compiler.pack_validator import validate_pack_manifest
from odin.compiler.pack_loader import load_pack_shadow
from odin.compiler.aot_compiler import compile_aot_shadow
from odin.compiler.cached_jit_compiler import compile_cached_capability_shadow


def test_fairy_story_requires_ystar_ref_and_non_executable_boundary():
    story = FairyStoryShadow("F1", "House", "Maria tells the safe house.", "YSTAR-1", ("gatekeeper",))
    assert validate_fairy_story_shadow(story) == []
    bad = FairyStoryShadow("F2", "Bad", "direct_apply", "", ("gatekeeper",))
    errors = validate_fairy_story_shadow(bad)
    assert "missing_ystar_unit_ref" in errors
    assert "forbidden_marker:direct_apply" in errors


def test_ystar_unit_preserves_candidate_and_app_authority():
    unit = YStarNativeUnitShadow(
        unit_id="Y1",
        story_ref="F1",
        center={"candidate_only": True, "app_authority": "preserve", "final_gate": "odin"},
        rings=("R0", "R1"),
        flow=("receive", "validate", "candidate"),
        forbidden=("app_mutation", "external_send"),
        emits=("shadow_runtime_flow",),
    )
    assert validate_ystar_unit_shadow(unit) == []


def test_narrative_aorta_node_maps_to_runtime_contract():
    node = NarrativeAortaNodeShadow(
        node_id="aorta.weaver.red_threads",
        fairy_label="The weaver gathers the red threads",
        ystar_node_ref="context_distillery.build_context_capsule",
        runtime_contract_ref="odin_context_capsule",
        ring="R3",
        authority_posture="context_only",
        forbidden_edges=("app_apply", "external_send", "invent_facts"),
        output_artifacts=("context_capsule",),
        trace_label="context.red_threads",
    )
    assert validate_aorta_node_shadow(node) == []


def test_fairy_mapping_lowers_to_shadow_fragment_with_forbidden_edges():
    mapping = FairyShadowMapping("weaver", "context", "odin_context_capsule", "candidate_only", ("invent_facts",), "context_shadow")
    fragment = lower_mapping_to_shadow_fragment(mapping)
    assert fragment["claim_boundary"] == "shadow_ir_fragment_is_blueprint_only"
    assert "app_mutation" in fragment["forbidden"]
    assert "external_send" in fragment["forbidden"]


def test_ystar_mediation_directive_preserves_boundaries():
    directive = YStarMediationDirectiveShadow(
        directive_id="D1",
        ystar_unit_ref="Y1",
        target_shadow_modules=("universal_work_shadow",),
        runtime_boundaries={"candidate_only": True, "no_app_mutation": True, "no_external_send": True, "final_gate_required": True},
        compile_hints={"resource_profile": "standard_local"},
        holes=(),
        risk={"authority_drift": "low"},
    )
    assert validate_ystar_mediation_shadow(directive) == []


def test_runtime_pack_manifest_validates_before_load():
    manifest = build_pack_manifest("standard_local", "standard_local", ["universal_work"])
    assert validate_pack_manifest(manifest) == []
    assert load_pack_shadow(manifest)["loaded"] is True
    bad = dict(manifest)
    bad["forbidden_capabilities"] = []
    assert load_pack_shadow(bad)["loaded"] is False


def test_aot_and_cached_capability_compilers_are_shadow_only():
    aot = compile_aot_shadow("standard_local", "standard_local", ["universal_work"])
    assert aot["status"] == "compiled_shadow"
    cached = compile_cached_capability_shadow("app1", "standard_local", ["universal_work", "direct_apply"])
    assert "direct_apply" not in cached["manifest"]["capabilities"]
