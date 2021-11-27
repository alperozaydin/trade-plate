import click


def is_confirmed():
    return click.confirm(
        "Do you want to perform these orders?\n"
        "\tTrade Plate will perform the actions described above.\n"
        "\tOnly 'y/yes' will be accepted to approve.\n\n"
        "\tEnter a value:"
    )
