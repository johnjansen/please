import sys
import click
from rich.console import Console
from rich.prompt import Confirm
from typing import List

console = Console()

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
    import subprocess

    try:
        if not natural_command:
            console.print("[yellow]Please provide a command, e.g.:[/yellow]")
            console.print("please list all text files")
            console.print("please show system memory usage")
            sys.exit(1)

        command_str = " ".join(natural_command)
        processor = CommandProcessor()

        result = processor.process(command_str)
        console.print(result)

        # If --execute flag is set or user confirms, run the command
        suggested_command = result.renderable.strip('`bash\n')  # Clean the command string
        if execute or Confirm.ask("Execute this command?", default=False):
            console.print("\n[yellow]Executing command...[/yellow]")
            # Use os.system to maintain shell state
            import os
            os.system(suggested_command)

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    cli()
