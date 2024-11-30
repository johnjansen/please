import sys
import click
from rich.console import Console
from rich.prompt import Confirm

console = Console()

@click.group()
def cli():
    """Natural language command-line assistant"""
    pass

@cli.command()
@click.argument('command', nargs=-1, required=True)
@click.option('--execute', '-e', is_flag=True, help="Automatically execute the suggested command")
def run(command: tuple, execute: bool):
    """Convert natural language to bash command"""
    from ..core.processor import CommandProcessor
    import subprocess

    try:
        command_str = " ".join(command)
        processor = CommandProcessor()

        result = processor.process(command_str)
        console.print(result)

        # If --execute flag is set or user confirms, run the command
        suggested_command = result.renderable  # Get the command from the panel
        if execute or Confirm.ask("Execute this command?", default=False):
            console.print("\n[yellow]Executing command...[/yellow]")
            subprocess.run(suggested_command, shell=True)

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        sys.exit(1)
