from click.testing import CliRunner
from please.cli.main import cli

def test_cli_help():
    """Test that CLI help works"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Natural language command-line assistant' in result.output

def test_cli_run_empty():
    """Test that running with no command shows error"""
    runner = CliRunner()
    result = runner.invoke(cli, ['run'])
    assert result.exit_code != 0
    assert 'Error' in result.output
