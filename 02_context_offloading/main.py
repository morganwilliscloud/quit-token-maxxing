"""DEMO 2: Context offloading — store large tool results externally, retrieve on demand.

Builds on Demo 1 by adding the ContextOffloader plugin alongside summarization.
"""

import datetime
import random

from strands import Agent, tool
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.vended_plugins.context_offloader import ContextOffloader, FileStorage


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
# Context offloading handles individual large tool results that would blow
# up the window on their own.
agent = Agent(
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3,
        preserve_recent_messages=10,
    ),
    plugins=[
        ContextOffloader(
            storage=FileStorage("./artifacts/"),  # or S3Storage for production
            max_result_tokens=2_500,   # offload anything bigger than this
            preview_tokens=500,        # what stays in context
            include_retrieval_tool=True,
        )
    ],
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
