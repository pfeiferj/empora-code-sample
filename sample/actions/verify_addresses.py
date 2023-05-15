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

    # Split addresses into chunks of MAX_ENTRIES_PER_REQUEST
    address_chunks = [addresses[i : i + MAX_ENTRIES_PER_REQUEST] for i in range(0, len(addresses), 100)]

    # Verify each chunk of addresses with smarty api
    verified_addresses = []
    for chunk in address_chunks:
        # Convert addresses to smarty api address input to validate against api limits
        # We also set match to invalid to simplify matching requests to results
        # Finally we set the input_id so we can match up requests after
        # filtering our input

        input_addresses = [USAddressInput.from_address(chunk[i], match="invalid", input_id=str(i)) for i in range(0,len(chunk))]

        # get input body from filtered addresses
        body = [address.dict() for address in input_addresses if address.is_valid()]


        # verify addresses with smarty api
        res = requests.post(f"{settings.smarty_api_base_route}/street-address", json=body, params=params)

        # Initialize response to invalid addresses
        chunk_response = [Address(street="",city="",zipcode="",valid=False)] * len(chunk)

        # Convert smarty response to internal address model
        # and match response to correct index in chunk
        for address in res.json():
            chunk_response[int(address["input_id"])] = USAddressOutput.parse_obj(address).to_address()

        # add chunk addresses to final list
        verified_addresses += chunk_response

    # Map the requested addresses to the matching verified addresses
    return list(partition(2, interleave([addresses, verified_addresses])))
