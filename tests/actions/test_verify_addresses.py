from unittest import TestCase, main
from requests_mock import Mocker
from tests.data.smarty_address_verification import mock_successful_response as mock_successful_address_response
from tests.data.addresses import basic_address_list
from sample.models.address import Address
from toolz.itertoolz import interleave, partition
from sample.actions.verify_addresses import verify_addresses


class TestVerifyAddresses(TestCase):
    @Mocker()
    def test_verify_addresses(self, requests_mock):
        mock_successful_address_response(requests_mock)
        addresses = basic_address_list()
        verified_addresses = verify_addresses(addresses)
        expected_verified_addresses = [
            Address(street="143 E Main St", city="Columbus", zipcode="43215-5370", valid=True),
            Address(street="1 Empora St", city="Title", zipcode="11111", valid=False),
        ]
        expected_result = list(partition(2, interleave([addresses, expected_verified_addresses])))
        self.assertEqual(verified_addresses, expected_result)


if __name__ == "__main__":
    main()
