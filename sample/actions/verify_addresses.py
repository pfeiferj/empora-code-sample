import requests
from toolz.itertoolz import interleave, partition
from typing import List, Tuple
from sample.models.address import Address
from sample.models.smarty.us_street_address import USAddressInput, USAddressOutput
from sample.models.settings import settings


MAX_ENTRIES_PER_REQUEST = 100


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

    # Initialize list of verified addresses with invalid addresses
    verified_addresses = [Address(street="", city="", zipcode="", valid=False)] * len(addresses)

    # Convert addresses to smarty api address input to validate against api
    # limits. We set match to invalid and the input_id to make it easier to
    # match addresses later
    input_addresses = [
        USAddressInput.from_address(addresses[i], match="invalid", input_id=str(i)) for i in range(0, len(addresses))
    ]

    # Filter out invalid addresses
    input_addresses = [address.dict() for address in input_addresses if address.is_valid()]

    # Split addresses into chunks of MAX_ENTRIES_PER_REQUEST
    address_chunks = [input_addresses[i : i + MAX_ENTRIES_PER_REQUEST] for i in range(0, len(input_addresses), 100)]

    # Verify each chunk of addresses with smarty api
    for chunk in address_chunks:
        # verify addresses with smarty api
        res = requests.post(f"{settings.smarty_api_base_route}/street-address", json=chunk, params=params)

        # Convert smarty response to internal address model
        # and match response to correct index in chunk
        for address in res.json():
            verified_addresses[int(address["input_id"])] = USAddressOutput.parse_obj(address).to_address()

    # Map the requested addresses to the matching verified addresses
    return list(partition(2, interleave([addresses, verified_addresses])))
