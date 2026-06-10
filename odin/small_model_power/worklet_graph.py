def build_worklet_graph(work: dict) -> dict:
    return {'artifact_kind':'odin_worklet_graph','protocol_version':'7.1','graph_id':'WG-'+work.get('work_id','UNKNOWN'),'work_id':work.get('work_id'),'nodes':[],'edges':[],'claim_boundary':'worklet_graph_candidate_only'}
