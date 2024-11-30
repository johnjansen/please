from typing import Optional
import openai
from rich.panel import Panel
from rich.console import Console
from ..models.command import Command
from ..utils.parser import parse_command

class CommandProcessor:
    """
    Processes natural language commands and converts them into bash commands
    using OpenAI's API.
    """

    def __init__(self):
        # Initialize OpenAI client (requires OPENAI_API_KEY environment variable)
        self.openai = openai.OpenAI()

    def _get_bash_command(self, query: str) -> str:
        """
        Convert natural language query to bash command using OpenAI.

        Args:
            query: Natural language description of what user wants to do

        Returns:
            Suggested bash command(s)
        """
        system_prompt = """
        You are a helpful CLI assistant that converts natural language queries
        into bash commands. Provide only the command, no explanations unless
        specifically asked. If multiple commands are needed, join them with &&.
        Ensure commands are safe and won't cause damage. If a command could be
        dangerous, return a warning instead of the command.
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
        """Process a natural language command and return suggested bash command."""
        if not command_text.strip():
            raise ValueError("Please provide a command")

        suggested_command = self._get_bash_command(command_text)

        # Create a nice panel with the suggestion
        return Panel(
            suggested_command,
            title="💡 Suggested Command",
            subtitle="Press Enter to execute or Ctrl+C to cancel",
            border_style="blue",
            padding=(1, 2)
        )
