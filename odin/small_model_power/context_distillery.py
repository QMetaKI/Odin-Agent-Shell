def build_context_capsule(work: dict) -> dict:
    return {'artifact_kind':'odin_context_capsule','work_id':work.get('work_id'),'claim_boundary':work.get('claim_boundary')}
