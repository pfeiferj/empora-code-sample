import click
from sample.commands.verify_addresses import verify_addresses

RED = "\u001b[31m"
CLEAR = "\u001b[0m"


def red(text: str) -> str:
    """
    Wraps the text in red ANSI escape codes.
    """
    return f"{RED}{text}{CLEAR}"


def main():
    # For now we only support one command so we'll call it here.
    # In the future if we need more commands we can use click's command groups:
    # @click.group()
    # def entry_point():
    #    pass
    # entry_point.add_command(command_1)
    # entry_point.add_command(command_2)
    # entry_point()
    try:
        verify_addresses()
    except Exception as e:
        with click.Context(verify_addresses) as ctx:
            click.echo(
                red(f"{e}\n"),
                err=True,
            )
            click.echo(verify_addresses.get_help(ctx))
