"""DEMO 4: Subagents — the agent-as-a-tool pattern for context isolation."""
# /// script
# requires-python = ">=3.11"
# dependencies = ["strands-agents==1.55.1"]
# ///

import datetime
import random

from strands import Agent, tool


# ---------------------------------------------------------------------------
# Tool stubs that simulate noisy infrastructure data
# ---------------------------------------------------------------------------

@tool
def read_logs(service_name: str, num_lines: int = 200) -> str:
    """Read recent log lines for a service.

    Args:
        service_name: Name of the service to get logs for.
        num_lines: Number of recent log lines to retrieve.
    """
    messages = [
        "INFO Request processed in {ms}ms",
        "INFO Health check passed",
        "WARN Retrying request (attempt {n}/3)",
        "ERROR Timeout waiting for downstream service: payment-api",
        "ERROR Failed to connect to database: connection refused",
    ]
    now = datetime.datetime.now()
    return "\n".join(
        f"[{(now - datetime.timedelta(seconds=num_lines - i)).isoformat()}] "
        + random.choice(messages).format(ms=random.randint(50, 5000), n=random.randint(1, 3))
        for i in range(num_lines)
    )


@tool
def get_metrics(service_name: str, metric: str, minutes: int = 30) -> str:
    """Fetch time-series metrics for a service.

    Args:
        service_name: Name of the service to query.
        metric: Metric name (e.g. latency_p99, error_rate, cpu_usage).
        minutes: How many minutes of data to return.
    """
    now = datetime.datetime.now()
    rows = []
    for i in range(minutes):
        ts = (now - datetime.timedelta(minutes=minutes - i)).strftime("%H:%M")
        if metric == "error_rate":
            value = round(random.uniform(0.1, 12.0), 2)
        elif metric == "latency_p99":
            value = random.randint(80, 4500)
        else:
            value = round(random.uniform(20, 95), 1)
        rows.append(f"{ts}  {service_name}/{metric}  {value}")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Subagents — each gets its own isolated context window
# ---------------------------------------------------------------------------

log_analyzer = Agent(
    name="analyze_logs",
    description="Analyze logs for a service and return a diagnosis.",
    tools=[read_logs],
    system_prompt=(
        "You are a log analysis specialist. Read the relevant logs and return "
        "ONLY a short diagnosis: summary, key findings, recommended actions. "
        "Never include raw log lines in your answer."
    ),
)

metrics_analyzer = Agent(
    name="analyze_metrics",
    description="Analyze metrics for a service and return an assessment.",
    tools=[get_metrics],
    system_prompt=(
        "You are a metrics analysis specialist. Query the relevant metrics "
        "and return ONLY a short assessment: which metrics are abnormal, "
        "how they correlate, and what they suggest. Never dump raw data points."
    ),
)

# ---------------------------------------------------------------------------
# Orchestrator — pass agents directly as tools
# ---------------------------------------------------------------------------

orchestrator = Agent(
    tools=[log_analyzer, metrics_analyzer],
    system_prompt=(
        "You are a senior SRE. Use your specialized agents to investigate "
        "services, then synthesize findings into concise, actionable recommendations."
    ),
)

if __name__ == "__main__":
    print("--- Turn 1: subagents do the noisy work")
    print(orchestrator(
        "The payment service is timing out intermittently. "
        "Check both the logs and the metrics."
    ))

    print("\n--- Turn 2: parent context stays clean")
    print(orchestrator("What's the most likely root cause and what should we do first?"))
    print(f"\n[parent message history length: {len(orchestrator.messages)}]")
