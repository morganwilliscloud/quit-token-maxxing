# Context Engineering Techniques for AI Agents

Code samples for the video: **Quit Tokenmaxxing: Context Engineering Techniques for AI Agents**

Context engineering is the practice of being intentional about what data makes it into your agent's context window, controlling how long it stays there, and managing that information so the agent stays focused and efficient. You apply it through agent harness design: the surrounding system that determines what context, tools, memory, and instructions the agent has access to as it works.

## The one-liner

```python
from strands import Agent

agent = Agent(context_manager="auto")
```

This combines several context engineering patterns with benchmark-validated defaults: large tool results are offloaded and replaced with previews, and older conversation is proactively summarized as the window fills up. On real code investigation tasks, this configuration dropped costs 55% while accuracy went from 68% to 98%. See the [benchmark post](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/).

The demos below break down the patterns behind that one line.

## Four categories

| Category | What it does |
|----------|-------------|
| Compress | Reduce tokens in the context window through compaction, like summarization |
| Externalize | Persist information outside the context window (files, databases) |
| Select | Give the agent ways to retrieve only what's relevant to the task |
| Isolate | Run tasks across multiple agents so each only sees what it needs |

These categories aren't mutually exclusive. Techniques can span multiple categories, and production agents usually combine several.

## Model providers

Strands is model-provider agnostic. The `model=` param on `Agent()` is the only thing you change — all the context engineering techniques work the same regardless of provider. See [`model_providers.py`](./model_providers.py) for ready-to-run examples using Bedrock, Anthropic, OpenAI, Ollama, and LiteLLM.

The demos default to Bedrock but you can drop in whatever model makes the most sense for your setup — swap the `model=` argument and nothing else changes.

## Demos

| # | Demo | Category | Description |
|---|------|----------|-------------|
| 01 | [Summarization](./01_summarization/) | Compress | Keep recent history intact and summarize the older zone. Optionally use a cheaper model and a custom summarization prompt |
| 02 | [Context Offloading](./02_context_offloading/) | Externalize + Select | Offload large tool results to storage, leaving a preview plus a reference in context. The agent retrieves details on demand via a retrieval tool |
| 03 | [Skills](./03_skills/) | Externalize + Select | Progressive disclosure with the `AgentSkills` plugin: instructions load only when a skill is activated |
| 04 | [Subagents](./04_subagents/) | Isolate | Agent-as-a-tool pattern: the subagent's disposable context window absorbs the noise, and the parent gets only the conclusion |

## Bonus: prompt caching

Prompt caching reduces cost on repeated calls by reusing previously computed context. The same `cache_config` param works across providers — though not every provider supports every option.

**Bedrock:**
```python
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5",
    cache_config={"strategy": "auto"},
)
```

**Anthropic (direct):**
```python
from strands.models import AnthropicModel

model = AnthropicModel(
    model_id="claude-sonnet-4-5",
    cache_config={"strategy": "auto", "ttl": "5m"},
)
```

**OpenAI** — caching is automatic on eligible models (no config needed, but you can pass `cache_config` to align with the same pattern):
```python
from strands.models import OpenAIModel

model = OpenAIModel(model_id="gpt-4o")
```

**LiteLLM:**
```python
from strands.models import LiteLLMModel

model = LiteLLMModel(
    model_id="claude-sonnet-4-5",
    cache_config={"strategy": "auto"},
)
```

Engineer your context to keep it stable across requests, then let the provider cache the repeated parts.

## Quick start

Each demo is a self-contained script with inline dependency metadata. Run any of them with `uv` and it will handle the environment automatically:

```bash
uv run 01_summarization/main.py
uv run 02_context_offloading/main.py
uv run 03_skills/main.py
uv run 04_subagents/main.py
```

Or install manually and run with plain Python:

```bash
pip install strands-agents==1.55.1
python 01_summarization/main.py
```

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- AWS account with Bedrock model access enabled (Claude Sonnet 5 recommended)
- AWS credentials configured via environment or `~/.aws/credentials`

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

## Note on the API

The `ContextManager` and `Offload` classes used in these demos currently live under `strands.experimental.context_manager`. They will move to the top-level `strands` namespace in a future release. The demos are pinned to `strands-agents==1.55.1` while the API stabilizes.

## Links

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Strands Agents Documentation](https://strandsagents.com)
- [Context Management Benchmark Post](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/)

## License

MIT
