"""DEMO 1: Summarization — compress older history, keep recent history intact."""
# /// script
# requires-python = ">=3.11"
# dependencies = ["strands-agents==1.55.1"]
# ///
from strands import Agent
from strands.experimental.context_manager import ContextManager, Offload

# Tip: context_manager="auto" gives you opinionated defaults with zero config.
# Here we configure it explicitly so you can see what each knob does.
agent = Agent(
    context_manager=ContextManager(
        strategies=[
            # When the context window hits 85% utilization, summarize the
            # oldest messages into a single summary message.
            # The 2 most recent matching messages are never touched.
            Offload.summarize("*").when(utilization=0.85, preserve_recent=2),
        ],
        stash=False, 
    ),
    system_prompt="You are a research assistant.",
)

if __name__ == "__main__":
    turns = [
        "I'm researching the history of container orchestration. Start before Kubernetes.",
        "Now cover how Docker changed deployment.",
        "How did Kubernetes emerge and what problems did it solve?",
        "Summarize the full timeline we've covered.",
    ]

    for i, turn in enumerate(turns, 1):
        print(f"\n--- Turn {i}: {turn}")
        agent(turn)
        print(f"    [messages in context: {len(agent.messages)}]")
