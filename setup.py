from setuptools import setup, find_packages

setup(
    name="please-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "prompt-toolkit>=3.0.0",
        "openai>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "please=please.cli.main:cli"  # Note: changed from cli.main:cli to just main:cli
        ],
    },
    author="John Jansen",
    author_email="john.jansen@me.com",
    description="Natural language command-line assistant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/johnjansen/please",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
