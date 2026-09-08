"""DEMO 1: Summarization — compress older history, keep recent history intact."""
from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager

agent = Agent(
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3,            # summarize the oldest 30% when compaction runs
        preserve_recent_messages=10,  # the 10 most recent messages are never touched
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
