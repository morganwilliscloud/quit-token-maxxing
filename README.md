# Context Engineering Techniques for AI Agents

Code samples for the video: **Quit Tokenmaxxing: 4 Tips for Context Engineering**

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

## Demos

| # | Demo | Category | Description |
|---|------|----------|-------------|
| 01 | [Summarization](./01_summarization/) | Compress | Keep recent history intact and summarize the older zone. Optionally use a cheaper model and a custom summarization prompt |
| 02 | [Context Offloading](./02_context_offloading/) | Externalize + Select | `ContextOffloader` stores large tool results externally, leaving a preview plus a reference. The agent retrieves details on demand, so nothing is thrown away |
| 03 | [Skills](./03_skills/) | Externalize + Select | Progressive disclosure with the `AgentSkills` plugin: instructions load only when a skill is activated |
| 04 | [Subagents](./04_subagents/) | Isolate | Agent-as-a-tool pattern: the subagent's disposable context window absorbs the noise, and the parent gets only the conclusion |

## Bonus: prompt caching

Not context engineering exactly, since it doesn't change *what* goes into the context window, just how efficiently repeated context is processed. With Bedrock (the Strands default provider):

```python
from strands import Agent
from strands.models import BedrockModel

agent = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-sonnet-5",
        cache_config={"strategy": "auto"},
    ),
)
```

Engineer your context to keep it focused, then cache the parts that stay the same request to request.

## Quick start

```bash
# Install dependencies
pip install strands-agents strands-agents-tools

# Set up AWS credentials (Bedrock is the default model provider)
export AWS_BEDROCK_API_KEY=your_bedrock_api_key
# Or use standard AWS credentials:
# export AWS_ACCESS_KEY_ID=...
# export AWS_SECRET_ACCESS_KEY=...
# export AWS_REGION=us-west-2

# Run any demo
cd 01_summarization
python main.py
```

## Prerequisites

- Python 3.10+
- AWS account with Bedrock model access enabled (Claude Sonnet 5 recommended)
- `strands-agents` and `strands-agents-tools` packages

## Links

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Strands Agents Documentation](https://strandsagents.com)
- [Context Management Benchmark Post](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/)

## License

MIT
