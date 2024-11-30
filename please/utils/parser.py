from ..models.command import Command

def parse_command(command_text: str) -> Command:
    """Parse a natural language command into a Command object."""
    words = command_text.strip().split()
    if not words:
        raise ValueError("Empty command")

    action = words[0].lower()  # normalize to lowercase
    args = {'raw_args': ' '.join(words[1:])}

    return Command(
        action=action,
        args=args,
        raw_text=command_text
    )
