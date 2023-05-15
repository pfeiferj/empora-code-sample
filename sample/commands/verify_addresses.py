import click
import sys
from os import isatty
from typing import TextIO
from sample.actions.verify_addresses import verify_addresses as verify_addresses_action
from sample.actions.parse_addresses_csv import parse_addresses_csv



NO_FILE_PROVIDED = (
    "No file provided.\nPlease pass the file name as the first argument or pipe the file data to this command.\n"
)


@click.command()
@click.argument("file", required=False, type=click.File("r"))
def verify_addresses(file: TextIO):
    """
    Read in a csv file of addresses and outputs a formatted version or invalid
    """
    # check terminal type so we know how to read the file data
    interactive = isatty(sys.stdin.fileno())

    # Raise an exception if we're in an interactive terminal and do not have a file
    if interactive and file is None:
        raise Exception(NO_FILE_PROVIDED)
    elif interactive:
        file_data = file
    # If we are not in an interactive session we read the file data from std.in so that we can support piped data
    else:
        file_data = sys.stdin

    # read addresses from file
    addresses = parse_addresses_csv(file_data)

    # get verified addresses from smarty api
    verified_addresses = verify_addresses_action(addresses)

    # print formatted addresses
    for i in range(len(verified_addresses)):
        print(f"{verified_addresses[i][0].format()} -> {verified_addresses[i][1].format()}")
