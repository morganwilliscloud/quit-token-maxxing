"""DEMO 3: Skills — progressive disclosure of instructions via the AgentSkills plugin.

Builds on Demos 1+2 by adding skills alongside summarization and offloading.
"""
# /// script
# requires-python = ">=3.11"
# dependencies = ["strands-agents==1.55.1"]
# ///

from pathlib import Path

from strands import Agent, AgentSkills

# NOTE: will move to top-level `from strands import ContextManager, Offload` in a future release.
from strands.experimental.context_manager import ContextManager, Offload
from strands.storage import LocalFileStorage
from strands.vended_tools import file_editor, shell

SKILLS_DIR = Path(__file__).parent / "skills"

# All three techniques stacked:
# - Summarization keeps overall conversation history compact
# - Offloading handles big tool results (e.g. large file reads)
# - Skills load specialized instructions only when the task calls for them
agent = Agent(
    context_manager=ContextManager(
        strategies=[
            # Big tool results get offloaded; a 500-token preview stays in context.
            Offload.truncate(
                "tool_results",
                {"preview_tokens": 500},
            ).when(threshold=2500),
            # Compact older messages once the window is 85% full.
            Offload.summarize("*").when(utilization=0.85, preserve_recent=2),
        ],
        # Stash keeps originals on disk and gives the agent a retrieval tool.
        stash={
            "storage": LocalFileStorage("./artifacts/"),
            "retrieval_tool": True,
        },
    ),
    plugins=[
        AgentSkills(skills=str(SKILLS_DIR)),
    ],
    tools=[file_editor, shell],
    system_prompt=(
        "You are an engineering assistant. Activate the relevant skill "
        "before starting a specialized task."
    ),
)

if __name__ == "__main__":
    print("--- Task 1: triggers the code-review skill")
    print(agent(
        "Review this function:\n\n"
        "def get_user(user_id):\n"
        '    query = f"SELECT * FROM users WHERE id = {user_id}"\n'
        "    return db.execute(query)"
    ))

    print("\n--- Task 2: triggers the api-design skill (code-review instructions never loaded here)")
    print(agent("Design an API endpoint for managing user notifications."))
