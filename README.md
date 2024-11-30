# Please CLI

A natural language command-line assistant that translates English commands into bash commands using OpenAI's GPT models.

## Features

- Convert natural language into executable shell commands
- Maintain command history and context
- Smart command suggestions based on previous actions
- Built-in safety checks for potentially dangerous operations
- Interactive confirmation before executing commands
- Detailed command history with `please show last`

## Installation

```bash
# Install from PyPI
pip install please-cli

# Or install from source
git clone https://github.com/johnjansen/please
cd please
pip install -e .
```

## Usage

```bash
# Get help
please help

# Basic commands
please list all python files
please show system memory usage
please create a backup of config.json

# Use -e flag to execute immediately without confirmation
please -e find large files

# View details of last executed command
please show last
```

## Configuration

The CLI requires an OpenAI API key to be set in your environment:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Command History

Command history is stored in `~/.please_memory` and includes:
- Timestamp
- Original natural language command
- Generated bash command
- Execution success/failure
- Command output

## Development

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
python scripts/run_tests.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for details.
