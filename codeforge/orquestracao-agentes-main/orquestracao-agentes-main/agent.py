from pathlib import Path

from llm import call_llm


class Agent:

    def __init__(self, name):
        self.name = name
        self.directory = Path("agents") / name

    def load_instructions(self):
        agent_file = self.directory / "AGENTS.md"
        skill_file = self.directory / "SKILL.md"

        agent = agent_file.read_text(encoding="utf-8")
        skill = skill_file.read_text(encoding="utf-8")

        return f"""
{agent}

# SKILL

{skill}
"""

    def run(self, task, context=""):
        system_prompt = self.load_instructions()
        user_prompt = f"""
# TAREFA

{task}

# CONTEXTO

{context}
"""
        return call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )