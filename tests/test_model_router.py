from odin.models.model_router import choose_route

def test_default_route():
    assert choose_route("standard_local") == "3b_7b_8b_hybrid"

def test_low_memory():
    assert choose_route("low_memory_strict") == "3b_micro_critic_router"

def test_quality_route():
    assert choose_route("quality_local", latency_mode="draft", quality_target="premium") == "3b_13b_14b_quality_hybrid"
