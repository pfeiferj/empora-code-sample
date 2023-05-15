from io import StringIO
from typing import List, TextIO
from sample.models.address import Address
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def basic_address_list() -> List[Address]:
    return [
        Address(street="143 e Maine Street", city="Columbus", zipcode="43215"),
        Address(street="1 Empora St", city="Title", zipcode="11111"),
    ]


def basic_address_csv() -> TextIO:
    with open(f"{dir_path}/addresses.csv", "r") as f:
        return StringIO(f.read())
