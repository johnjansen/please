import sys
import os
import click
import tempfile
import subprocess
import re
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from typing import List

console = Console()

HELP_TEXT = """
🤖 Natural Language Command Assistant

Commands:
  • Any natural language command:
      please list all python files
      please show system memory usage

Built-in Commands:
  • show last         Show details of the last executed command
  • help              Show this help message

Options:
  -e, --execute       Automatically execute the command without confirmation
  --help             Show this message and exit

Examples:
  please list all text files
  please show system memory usage
  please show last
  please -e find large files
"""

def clean_command(command: str) -> str:
    """Clean command string from markdown code block markers without affecting the command itself"""
    # Remove ```bash and ``` markers carefully
    command = re.sub(r'^```bash\n', '', command)
    command = re.sub(r'\n```$', '', command)
    command = command.strip()
    return command

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('natural_command', nargs=-1, type=click.UNPROCESSED)
@click.option('--execute', '-e', is_flag=True, help="Automatically execute the suggested command")
@click.pass_context
def cli(ctx, natural_command: List[str], execute: bool):
    """Natural language command-line assistant"""
    from ..core.processor import CommandProcessor

    try:
        # Show help for no arguments or explicit help command
        if not natural_command or natural_command[0].lower() in ['help', '--help']:
            console.print(Panel(HELP_TEXT, title="📚 Please CLI Help", border_style="blue"))
            sys.exit(0)

        command_str = " ".join(natural_command)
        processor = CommandProcessor()

        result = processor.process(command_str)
        console.print(result)

        # Don't execute if it's the "show last" command
        if command_str.strip().lower() == "show last":
            return

        # If --execute flag is set or user confirms, run the command
        # If --execute flag is set or user confirms, run the command
        suggested_command = clean_command(result.renderable)

        # Auto-execute if it's just an echo command, otherwise ask for confirmation
        should_execute = (
            execute or
            suggested_command.startswith('echo ') or
            Confirm.ask("Execute this command?", default=False)
        )

        if should_execute:
            console.print("\n[yellow]Executing command...[/yellow]")

            # Get the user's current shell
            current_shell = os.environ.get('SHELL', '/bin/bash')

            # Execute and capture output
            process = subprocess.run(
                [current_shell, '-c', suggested_command],
                env=os.environ,
                text=True,
                capture_output=True
            )

            # Display output immediately
            if process.stdout:
                console.print(process.stdout)
            if process.stderr:
                console.print("[red]" + process.stderr + "[/red]")

            # Update command memory with result
            processor.update_last_result(
                success=(process.returncode == 0),
                result=process.stdout if process.stdout else None
            )

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    cli()
