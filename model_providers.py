"""Model providers — Strands is model-provider agnostic.

The same Agent code runs on any supported provider. Swap the model
passed to Agent() and everything else stays the same.

Requirements vary by provider — see the comments on each block.
Install the relevant package and set the required env var, then
copy the block you want into your own script.
"""

from strands import Agent

# ── AWS Bedrock (default) ─────────────────────────────────────────────────────
# No extra packages. Requires AWS credentials:
#   export AWS_ACCESS_KEY_ID=...
#   export AWS_SECRET_ACCESS_KEY=...
#   export AWS_DEFAULT_REGION=us-east-1
# Or use an IAM role / AWS SSO profile.

from strands.models import BedrockModel

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-5"),
)

# ── Anthropic (direct) ────────────────────────────────────────────────────────
# pip install anthropic
# export ANTHROPIC_API_KEY=...

# from strands.models import AnthropicModel
#
# agent = Agent(
#     model=AnthropicModel(
#         model_id="claude-sonnet-4-5",
#         client_args={"api_key": "..."},   # or omit to read ANTHROPIC_API_KEY
#         cache_config={"strategy": "auto", "ttl": "5m"},  # prompt caching supported
#     ),
# )

# ── OpenAI ────────────────────────────────────────────────────────────────────
# pip install openai
# export OPENAI_API_KEY=...
# OpenAI caches automatically on eligible models — no cache_config needed.

# from strands.models import OpenAIModel
#
# agent = Agent(
#     model=OpenAIModel(
#         model_id="gpt-4o",
#         client_args={"api_key": "..."},   # or omit to read OPENAI_API_KEY
#     ),
# )

# ── Ollama (local) ────────────────────────────────────────────────────────────
# Install Ollama: https://ollama.com
# ollama pull llama3.2
# pip install ollama

# from strands.models import OllamaModel
#
# agent = Agent(
#     model=OllamaModel(model_id="llama3.2"),
#     # cache_config accepted but has no effect on Ollama
# )

# ── LiteLLM (100+ providers via one interface) ────────────────────────────────
# pip install litellm
# Supports OpenAI, Anthropic, Cohere, Mistral, Groq, etc.
# See https://docs.litellm.ai/docs/providers for the full list.

# from strands.models import LiteLLMModel
#
# agent = Agent(
#     model=LiteLLMModel(
#         model_id="claude-sonnet-4-5",
#         cache_config={"strategy": "auto"},  # prompt caching supported
#     ),
#     # model=LiteLLMModel(model_id="gpt-4o"),
#     # model=LiteLLMModel(model_id="groq/llama-3.1-8b-instant"),
# )


# ── Everything else stays the same ───────────────────────────────────────────
# Context management, tools, skills, subagents — none of it changes.
# The model= param is the only thing you swap.

if __name__ == "__main__":
    print(agent("What model are you running on?"))
