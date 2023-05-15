from unittest import TestCase, main
from requests_mock import Mocker
from tests.data.smarty_address_verification import mock_successful_response as mock_successful_address_response
from tests.data.addresses import basic_address_list
from sample.models.address import Address
from toolz.itertoolz import interleave, partition
from sample.actions.verify_addresses import (
    verify_addresses,
    get_smarty_zipcode,
    get_smarty_street,
    get_smarty_city,
    is_smarty_address_valid,
)


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

    def test_get_smarty_zipcode(self):
        data = {"components": {"zipcode": "11111", "plus4_code": "2222"}}
        self.assertEqual(get_smarty_zipcode(data), "11111-2222")

    def test_get_smarty_zipcode_no_plus_4(self):
        data = {"components": {"zipcode": "11111"}}
        self.assertEqual(get_smarty_zipcode(data), "11111")

    def test_get_smarty_street(self):
        data = {
            "components": {
                "primary_number": "143",
                "street_predirection": "E",
                "street_name": "Main",
                "street_suffix": "St",
            }
        }
        self.assertEqual(get_smarty_street(data), "143 E Main St")

    def test_get_smarty_street_no_predirection(self):
        data = {
            "components": {
                "primary_number": "143",
                "street_name": "Main",
                "street_suffix": "St",
            }
        }
        self.assertEqual(get_smarty_street(data), "143 Main St")

    def test_get_smarty_street_no_suffix(self):
        data = {
            "components": {
                "primary_number": "143",
                "street_name": "Main",
            }
        }
        self.assertEqual(get_smarty_street(data), "143 Main")

    def test_get_smarty_city(self):
        data = {
            "components": {
                "city_name": "Columbus",
            }
        }
        self.assertEqual(get_smarty_city(data), "Columbus")

    def test_is_smarty_address_valid(self):
        data = {
            "analysis": {
                "dpv_match_code": "Y",
            }
        }
        valid = is_smarty_address_valid(data)
        self.assertTrue(valid)

    def test_is_smarty_address_valid_not_in_usps(self):
        data = {
            "analysis": {
                "dpv_match_code": "",
            }
        }
        valid = is_smarty_address_valid(data)
        self.assertFalse(valid)

    def test_is_smarty_address_valid_ignored_secondary(self):
        data = {
            "analysis": {
                "dpv_match_code": "S",
            }
        }
        valid = is_smarty_address_valid(data)
        self.assertTrue(valid)

    def test_is_smarty_address_valid_missing_secondary(self):
        data = {
            "analysis": {
                "dpv_match_code": "D",
            }
        }
        valid = is_smarty_address_valid(data)
        self.assertTrue(valid)


if __name__ == "__main__":
    main()
