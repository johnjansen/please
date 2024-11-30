from typing import Optional
import openai
from rich.panel import Panel
from rich.console import Console
from ..models.command import Command
from ..utils.parser import parse_command

class CommandProcessor:
    def __init__(self):
        self.openai = openai.OpenAI()

    def _get_bash_command(self, query: str) -> str:
        system_prompt = """
        You are a helpful CLI assistant that converts natural language queries
        into bash commands. Return ONLY the command wrapped in ```bash
        command here
        ``` markers. No other text or explanations unless specifically asked.
        If multiple commands are needed, join them with &&.
        If a command could be dangerous, return a warning instead.
        """

        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Convert this to a bash command: {query}"}
                ],
                temperature=0.7,
                max_tokens=100
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise ValueError(f"Error getting command suggestion: {str(e)}")

    def process(self, command_text: str) -> Panel:
        if not command_text.strip():
            raise ValueError("Please provide a command")

        suggested_command = self._get_bash_command(command_text)

        return Panel(
            suggested_command,
            title="💡 Suggested Command",
            subtitle="Press Enter to execute or Ctrl+C to cancel",
            border_style="blue",
            padding=(1, 2)
        )
