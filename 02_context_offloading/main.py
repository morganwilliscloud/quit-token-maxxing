"""DEMO 2: Context offloading — store large tool results externally, retrieve on demand.

Builds on Demo 1 by adding an offload strategy for tool results alongside summarization.
"""
# /// script
# requires-python = ">=3.11"
# dependencies = ["strands-agents==1.55.1"]
# ///

import datetime
import random

from strands import Agent, tool
from strands.experimental.context_manager import ContextManager, Offload
from strands.storage import LocalFileStorage


@tool
def get_service_logs(service_name: str, num_lines: int = 500) -> str:
    """Fetch recent log lines for a service.

    Args:
        service_name: Name of the service to get logs for.
        num_lines: Number of recent log lines to retrieve.
    """
    messages = [
        "INFO Request processed in {ms}ms",
        "INFO Cache hit ratio: {pct}%",
        "WARN Retrying request (attempt {n}/3)",
        "ERROR Timeout waiting for downstream service: payment-api",
        "ERROR Failed to connect to database: connection refused",
    ]
    now = datetime.datetime.now()
    return "\n".join(
        f"[{(now - datetime.timedelta(seconds=num_lines - i)).isoformat()}] "
        + random.choice(messages).format(
            ms=random.randint(50, 5000), pct=random.randint(10, 99), n=random.randint(1, 3)
        )
        for i in range(num_lines)
    )


# Summarization (from Demo 1) keeps overall conversation history manageable.
# The truncate strategy handles individual large tool results — anything over
# ~2,500 tokens gets offloaded to disk, a 500-token preview stays in context.
# The stash config wires up FileStorage and enables a retrieval tool so the
# agent can pull back the full content when it needs specific details.
agent = Agent(
    context_manager=ContextManager(
        strategies=[
            # Tool results over ~2,500 tokens get offloaded; a 500-token
            # head/tail preview stays in the context window.
            Offload.truncate(
                "tool_results",
                {"preview_tokens": 500},
            ).when(threshold=2500),
            # Same summarization policy as Demo 1.
            Offload.summarize("*").when(utilization=0.85, preserve_recent=2),
        ],
        # Storage backend for offloaded content. The retrieval tool (get_context)
        # is automatically added to the agent so it can fetch originals on demand.
        # Omit `stash` entirely to use in-memory storage instead.
        stash={
            "storage": LocalFileStorage("./artifacts/"),  # or S3Storage for production
            "retrieval_tool": True,
        },
    ),
    tools=[get_service_logs],
    system_prompt=(
        "You are an incident triage agent. Investigate issues by pulling logs "
        "and retrieving offloaded details when you need them."
    ),
)

if __name__ == "__main__":
    print("--- Turn 1: big tool result gets offloaded")
    print(agent("The payment service is timing out. Pull its logs and give me a first read."))

    print("\n--- Turn 2: agent retrieves details from storage, not from context")
    print(agent("What were the exact timestamps of the database connection errors?"))
