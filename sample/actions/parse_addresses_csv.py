import csv

from typing import List, TextIO
from sample.models.address import Address

def parse_addresses_csv(csv_file: TextIO) -> List[Address]:
    """
    Takes a csv file and parses it into a list of addresses
    """

    # create a csv reader from the file data
    reader = csv.reader(csv_file)

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
