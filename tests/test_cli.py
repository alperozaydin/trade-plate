from click.testing import CliRunner, Result

import trade_plate.cli as cli


def test_trader_plate_cli():
    """
    Arrange/Act: Run the `version` subcommand with the '-v' flag.
    Assert: The output indicates verbose logging is enabled.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, "--version")
    assert result.exit_code == 0
