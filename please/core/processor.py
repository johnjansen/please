import os
import json
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path
import openai
import tiktoken
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from ..models.command import Command
from ..models.memory import CommandMemory
from ..utils.parser import parse_command

class CommandProcessor:
    MAX_CONTEXT_TOKENS = 2000

    def __init__(self):
        self.openai = openai.OpenAI()
        self.memory_file = Path(os.path.expanduser("~/.please_memory"))
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.last_command = self._load_memory()

    def _load_memory(self) -> Optional[CommandMemory]:
        """Load the last command from memory file"""
        try:
            if self.memory_file.exists():
                data = json.loads(self.memory_file.read_text())
                return CommandMemory(
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    natural_command=data['natural_command'],
                    bash_command=data['bash_command'],
                    successful=data['successful'],
                    result=data.get('result')
                )
        except Exception as e:
            console = Console()
            console.print(f"[yellow]Warning:[/yellow] Could not load memory: {e}")
            return None
        return None

    def _save_memory(self, memory: CommandMemory):
        """Save command to memory file"""
        try:
            data = {
                'timestamp': memory.timestamp.isoformat(),
                'natural_command': memory.natural_command,
                'bash_command': memory.bash_command,
                'successful': memory.successful,
                'result': memory.result
            }
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            self.memory_file.write_text(json.dumps(data))
            self.last_command = memory
        except Exception as e:
            console = Console()
            console.print(f"[yellow]Warning:[/yellow] Could not save memory: {e}")

    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in a string"""
        return len(self.encoding.encode(text))

    def _truncate_result(self, result: str, max_tokens: int) -> str:
        """Truncate result to fit within token limit"""
        if not result:
            return result

        tokens = self.encoding.encode(result)
        if len(tokens) <= max_tokens:
            return result

        # Take the last `max_tokens` tokens
        truncated_tokens = tokens[-max_tokens:]
        return self.encoding.decode(truncated_tokens) + "\n[truncated...]"

    def _get_context(self, query: str) -> str:
        """
        Get context from memory, respecting token limits.
        Reserves tokens for the system prompt, query, and response.
        """
        if not self.last_command:
            return ""

        # Calculate available tokens for context
        system_prompt_tokens = self._count_tokens(self.SYSTEM_PROMPT)
        query_tokens = self._count_tokens(query)
        reserved_tokens = system_prompt_tokens + query_tokens + 500  # Reserve 500 for response
        available_tokens = self.MAX_CONTEXT_TOKENS - reserved_tokens

        if available_tokens <= 0:
            return ""

        # Build context with the last command
        context_parts = []

        # Add basic command info
        basic_info = f"""
        Last command: {self.last_command.bash_command}
        Was successful: {self.last_command.successful}
        """
        context_parts.append(basic_info)

        # If we have result and room for it, add truncated result
        if self.last_command.result:
            current_tokens = self._count_tokens("".join(context_parts))
            result_tokens_available = available_tokens - current_tokens

            if result_tokens_available > 100:  # Only include if we can show meaningful amount
                truncated_result = self._truncate_result(
                    self.last_command.result,
                    result_tokens_available
                )
                context_parts.append(f"Result: {truncated_result}")

        return "\n".join(context_parts)

    SYSTEM_PROMPT = """
    You are a helpful CLI assistant that converts natural language inputs into bash commands.

    If the input is a question or requires explanation:
    - Return a command that echoes an informative response
    - Format: ```bash
    echo 'Your informative response here'
    ```

    If the input is an action request:
    - Return the appropriate bash command
    - Format: ```bash
    actual_command --with --flags
    ```

    Return ONLY the command, no other text or explanations.
    If multiple commands are needed, join them with &&.
    If a command could be dangerous, return an echo warning instead.

    Context from last command (if relevant):
    {context}
    """

    def _get_bash_command(self, query: str) -> str:
        context = self._get_context(query)

        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT.format(context=context)
                    },
                    {
                        "role": "user",
                        "content": f"Convert this to a bash command: {query}"
                    }
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

        # Special command to show last command
        if command_text.strip().lower() == "show last":
            if not self.last_command:
                return Panel("No previous command found", title="🕒 Command History", border_style="yellow")

            table = Table(show_header=True)
            table.add_column("Detail", style="cyan")
            table.add_column("Value", style="white")

            table.add_row("Timestamp", self.last_command.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            table.add_row("Natural Command", self.last_command.natural_command)
            table.add_row("Bash Command", self.last_command.bash_command)
            table.add_row("Successful", "✅" if self.last_command.successful else "❌")
            if self.last_command.result:
                table.add_row("Result", self.last_command.result)

            return Panel(table, title="🕒 Last Command", border_style="blue", padding=(1, 2))

        suggested_command = self._get_bash_command(command_text)

        # Strip the markdown code block markers
        clean_command = suggested_command.replace('```bash', '').replace('```', '').strip()

        # Create a memory object for the new command
        memory = CommandMemory(
            timestamp=datetime.now(),
            natural_command=command_text,
            bash_command=clean_command,
            successful=False  # Will be updated after execution
        )
        self._save_memory(memory)

        return Panel(
            suggested_command,
            title="💡 Suggested Command",
            subtitle="Press Enter to execute or Ctrl+C to cancel",
            border_style="blue",
            padding=(1, 2)
        )

    def update_last_result(self, success: bool, result: Optional[str] = None):
        """Update the last command with its execution result"""
        if self.last_command:
            self.last_command.successful = success
            self.last_command.result = result
            self._save_memory(self.last_command)
