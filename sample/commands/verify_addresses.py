import click
import sys
from os import isatty
from io import StringIO
from typing import List, TextIO
from sample.models.address import Address
from sample.actions.verify_addresses import verify_addresses as verify_addresses_action

import csv


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


def parse_addresses_csv(csv_file: TextIO) -> List[Address]:
    """
    Takes a csv file and parses it into a list of addresses
    """

    # create a csv reader from the file data
    data_io = StringIO(str(csv_file.read()))
    reader = csv.reader(data_io)

    # read from the csv reader into an addresses list
    addresses: List[Address] = []
    line_no = 0
    for row in reader:
        line_no += 1
        if len(row) != 3:
            raise Exception(f"Invalid address row on line number: {line_no}.")
        addresses.append(Address(street=row[0], city=row[1], zipcode=row[2]))

    # strip header if present
    if len(addresses) != 0 and addresses[0].is_header():
        addresses = addresses[1:]

    # verify we have addresses
    if len(addresses) == 0:
        raise Exception("No addresses found in file.")

    return addresses
