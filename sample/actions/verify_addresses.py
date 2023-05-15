import requests
from toolz import dicttoolz, itertoolz
from typing import List, Tuple
from sample.models.address import Address
from sample.models.smarty.us_street_address import USAddressInput
from sample.models.settings import settings

get_in = dicttoolz.get_in
interleave = itertoolz.interleave
partition = itertoolz.partition

MAX_ENTRIES_PER_REQUEST = 100
MAX_PAYLOAD_SIZE = 32 * 1024  # 32KB


def verify_addresses(addresses: List[Address]) -> List[Tuple[Address, Address]]:
    """
    Takes a list of addresses and verifies them against the smarty street
    address api and then returns a list of tuples where the first element in the
    tuple is the original address and the second element is the validated and
    corrected address.
    """
    # Authentication parameters for smarty api
    params = {
        "auth-id": settings.smarty_api_id,
        "auth-token": settings.smarty_api_key,
        "license": settings.smarty_api_license,
    }

    # Split addresses into chunks of 100
    address_chunks = [addresses[i:i+100] for i in range(0, len(addresses), 100)]

    # Verify each chunk of addresses with smarty api
    verified_addresses = []
    for chunk in address_chunks:
        # Convert addresses to smarty api address input to validate against api limits
        # We also set match to invalid to simplify matching requests to results
        body = [
            USAddressInput(street=address.street, city=address.city, zipcode=address.zipcode, match="invalid").dict()
            for address in chunk
        ]

        # verify addresses with smarty api
        res = requests.post(f"{settings.smarty_api_base_route}/street-address", json=body, params=params)

        # convert smarty response to internal address model
        verified_addresses += [smarty_address_to_address(address) for address in res.json()]

    # Map the requested addresses to the matching verified addresses
    return list(partition(2, interleave([addresses, verified_addresses])))


def smarty_address_to_address(smarty_address) -> Address:
    """
    Convert a smarty address response to an address model.
    """

    # Get each part of the internal address model
    street = get_smarty_street(smarty_address)
    city = get_smarty_city(smarty_address)
    zipcode = get_smarty_zipcode(smarty_address)
    valid = is_smarty_address_valid(smarty_address)

    return Address(street=street, city=city, zipcode=zipcode, valid=valid)


def get_smarty_city(smarty_address) -> str:
    """
    Retrieve the city from a smarty address response.
    """
    components = get_in(["components"], smarty_address, default={})

    # get the city component
    city_name = get_in(["city_name"], components, default="")

    return city_name


def get_smarty_street(smarty_address) -> str:
    """
    Retrieve the street address from a smarty address response.
    """
    components = get_in(["components"], smarty_address, default={})

    # get the street components
    primary_number = get_in(["primary_number"], components, default="")
    street_predirection = get_in(["street_predirection"], components, default="")
    street_name = get_in(["street_name"], components, default="")
    street_suffix = get_in(["street_suffix"], components, default="")

    # Build street from components excluding optional parts if missing
    street = primary_number
    if street_predirection != "":
        street += f" {street_predirection}"
    street += f" {street_name}"
    if street_suffix != "":
        street += f" {street_suffix}"

    return street


def get_smarty_zipcode(smarty_address) -> str:
    """
    Retrieve the zipcode from a smarty address response.
    """
    components = get_in(["components"], smarty_address, default={})

    # get the zipcode components
    zipcode = get_in(["zipcode"], components, default="")
    plus4_code = get_in(["plus4_code"], components, default="")

    # add plus4 if it exists
    if plus4_code != "":
        zipcode += f"-{plus4_code}"

    return zipcode


def is_smarty_address_valid(smarty_address) -> bool:
    """
    Checks a smarty_address response to see if the address is in the usps database.
    """
    # validation field
    match_code = get_in(["analysis", "dpv_match_code"], smarty_address, default="")

    # valid if address is in usps database
    valid = match_code in ["Y", "S", "D"]

    return valid
