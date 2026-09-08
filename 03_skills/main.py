"""DEMO 3: Skills — progressive disclosure of instructions via the AgentSkills plugin.

Builds on Demos 1+2 by adding skills alongside summarization and offloading.
"""

from pathlib import Path

from strands import Agent, AgentSkills
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.vended_plugins.context_offloader import ContextOffloader, FileStorage
from strands_tools import editor, file_read, file_write, shell

SKILLS_DIR = Path(__file__).parent / "skills"

# All three techniques stacked:
# - Summarization keeps overall conversation history compact
# - Offloading handles big tool results (e.g. file reads)
# - Skills load specialized instructions only when needed
agent = Agent(
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3,
        preserve_recent_messages=10,
    ),
    plugins=[
        ContextOffloader(
            storage=FileStorage("./artifacts/"),
            max_result_tokens=2_500,
            preview_tokens=500,
            include_retrieval_tool=True,
        ),
        AgentSkills(skills=str(SKILLS_DIR)),
    ],
    tools=[editor, file_read, file_write, shell],
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
