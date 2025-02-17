import pytest
from typer.testing import CliRunner

from cpdlog.cli import app

EXAMPLE = "examples/cpdlog.csv"


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_recent(runner):
    result = runner.invoke(app, ["recent", "--logfile", EXAMPLE])
    assert "There are 2 entries in the CPD Log File" in result.stdout
    assert "Example Training Course" in result.stdout
    assert result.exit_code == 0


def test_cli_summary(runner):
    result = runner.invoke(app, ["summary", "--logfile", EXAMPLE])
    assert "There are 2 entries in the CPD Log File" in result.stdout
    assert "Total for last 3 years:" in result.stdout
    assert result.exit_code == 0
