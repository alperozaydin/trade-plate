import pytest
from asyncclick.testing import CliRunner, Result

import trade_plate.cli as cli


@pytest.mark.asyncio
async def test_trader_plate_version():
    """
    Arrange/Act: Run the `version` subcommand with the '-v' flag.
    Assert: The output indicates verbose logging is enabled.
    """
    runner: CliRunner = CliRunner()
    result: Result = await runner.invoke(cli.cli, "--version")
    assert result.exit_code == 0
    assert "0.0.1" in result.output
