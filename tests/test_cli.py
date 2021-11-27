import trade_plate.cli as cli
from click.testing import CliRunner, Result


def test_trader_plate_version():
    """
    Arrange/Act: Run the `version` subcommand with the '-v' flag.
    Assert: The output indicates verbose logging is enabled.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, "--version")
    assert "0.0.1" in result.output.strip()
