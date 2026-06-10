# Shadow Runtime Resource and Provider Plan v7.1

## Resource Posture

The resource scheduler outputs a route ceiling. It does not use hardcoded hardware names. It uses abstract resource profiles:

- low_memory_strict
- standard_local
- quality_local
- heavy_local
- max_local_batch
- remote_optional

## Provider Adapter Plan

The provider adapter plan maps a route to an allowed provider surface:

- list_models
- profile_model
- run_model_work_packet
- cancel
- health

## Provider Boundaries

Mock, Ollama and llama.cpp are local-provider classes. Any remote-compatible provider requires explicit permission and privacy gates.

## Codex Conversion

Real targets:

- `odin/models/model_router.py`
- `odin/models/model_profiler.py`
- `odin/models/providers/mock.py`
- `odin/models/providers/ollama.py`
- `odin/models/providers/llama_cpp.py`
- `odin/models/providers/openai_compatible.py`

The shadow provider adapter must be implemented before live providers are wired.

## Route Ceiling Examples

- low_memory_strict: deterministic, 1B/2B and 3B micro routes only.
- standard_local: 3B + 7B/8B hybrid remains the default ceiling.
- quality_local: 13B/14B quality hybrid may be selected when latency mode is draft or batch.
- heavy_local: 22B/32B routes are allowed only for batch-like work.
- max_local_batch: 70B-class local/offload is never interactive by default.

## Provider Adapter Non-Claims

A provider adapter plan is not a provider call. The shadow object may describe how Ollama, llama.cpp or a mock provider should be invoked later, but it may not report model output, latency, token speed or success. Those values require real runtime receipts after implementation.

## Policy Coupling

Provider selection must be gated by caller policy, privacy class, model policy, resource posture, latency mode and claim boundary. Remote provider plans must remain blocked unless remote is explicit and the input artifacts are allowed for remote use.
