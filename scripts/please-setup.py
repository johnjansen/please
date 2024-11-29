#!/usr/bin/env python3
"""
please-setup.py
Script to create the initial directory structure and files for the 'please' CLI project.
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """
    Creates the complete directory structure for the please project, including
    all necessary files with basic content.
    """
    # Base project structure
    directories = [
        "please",                    # Main package directory
        "please/core",              # Core functionality
        "please/cli",               # CLI interface
        "please/utils",             # Utility functions
        "please/models",            # Data models
        "tests",                    # Test directory
        "tests/unit",               # Unit tests
        "tests/integration",        # Integration tests
        "docs",                     # Documentation
        "scripts",                  # Development and deployment scripts
    ]

    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create __init__.py in Python package directories
        if directory.startswith("please"):
            Path(f"{directory}/__init__.py").touch()

    # Create essential files
    files = {
        "setup.py": "# Package setup configuration",
        "README.md": "# Please CLI\n\nNatural language command-line assistant",
        "requirements.txt": "# Project dependencies",
        "please/__main__.py": "# Entry point for direct module execution",
        ".gitignore": """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.coverage
htmlcov/
        """.strip(),
        "tests/__init__.py": "",
        "please/cli/__init__.py": "",
        "please/core/__init__.py": "",
        "please/utils/__init__.py": "",
        "please/models/__init__.py": "",
    }

    # Create and populate files
    for file_path, content in files.items():
        with open(file_path, 'w') as f:
            f.write(content)

    print("✨ Project structure created successfully!")
    print("\nCreated directories:")
    os.system('tree -a -I "__pycache__"')

if __name__ == "__main__":
    try:
        create_directory_structure()
    except Exception as e:
        print(f"Error creating project structure: {e}", file=sys.stderr)
        sys.exit(1)
