from __future__ import annotations
def select_y_core_posture(latency_mode: str = "interactive", compiler_mode: bool = False) -> dict:
    posture = "compiler_core" if compiler_mode else ("low_memory_core" if latency_mode == "low_memory_strict" else "odin_llm_work_core")
    return {"artifact_kind":"odin_y_core_posture","posture_id":posture,"authority_scope":"odin_llm_work_only","app_authority_preserved":True,"odin_scope":["llm_admissibility","model_route","candidate_boundary","why_trace"],"rings":{"R0":"boundary","R1":"policy","R5":"seeds","R8":"model_route","R9":"candidate"}}
