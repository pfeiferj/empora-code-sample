from unittest import TestCase, main
from requests_mock import Mocker
from tests.data.smarty_address_verification import mock_successful_response, successful_response_data_1
from tests.data.addresses import basic_address_list
from sample.models.address import Address
from toolz.itertoolz import interleave, partition
from sample.actions.verify_addresses import verify_addresses
from sample.models.settings import settings


class TestVerifyAddresses(TestCase):
    @Mocker()
    def test_verify_addresses(self, requests_mock):
        mock_successful_response(requests_mock)
        addresses = basic_address_list()
        verified_addresses = verify_addresses(addresses)
        expected_verified_addresses = [
            Address(street="143 E Main St", city="Columbus", zipcode="43215-5370", valid=True),
            Address(street="1 Empora St", city="Title", zipcode="11111", valid=False),
        ]
        expected_result = list(partition(2, interleave([addresses, expected_verified_addresses])))
        self.assertEqual(verified_addresses, expected_result)

    @Mocker()
    def test_verify_addresses_200(self, requests_mock: Mocker):
        response_mock_data = []
        for i in range(0, 200):
            response_mock_data += successful_response_data_1()
            response_mock_data[-1]["input_id"] = str(i)

        requests_mock.post(f"{settings.smarty_api_base_route}/street-address", json=response_mock_data)

        addresses = [Address(street="143 e Maine Street", city="Columbus", zipcode="43215")] * 200
        verified_addresses = verify_addresses(addresses)
        expected_verified_addresses = [
            Address(street="143 E Main St", city="Columbus", zipcode="43215-5370", valid=True),
        ] * 200
        expected_result = list(partition(2, interleave([addresses, expected_verified_addresses])))
        self.assertEqual(verified_addresses, expected_result)
        self.assertEqual(requests_mock.call_count, 2)

    @Mocker()
    def test_verify_addresses_invalid(self, requests_mock: Mocker):
        # Test that order is maintained with an invalid address
        response_mock_data = []
        for i in range(0, 40):
            response_mock_data += successful_response_data_1()
            response_mock_data[-1]["input_id"] = str(i)
        del response_mock_data[23]

        requests_mock.post(f"{settings.smarty_api_base_route}/street-address", json=response_mock_data)

        addresses = [Address(street="143 e Maine Street", city="Columbus", zipcode="43215")] * 40
        addresses[23] = Address(street="a" * 70, city="Title", zipcode="11111")

        verified_addresses = verify_addresses(addresses)

        expected_verified_addresses = [
            Address(street="143 E Main St", city="Columbus", zipcode="43215-5370", valid=True),
        ] * 40
        expected_verified_addresses[23] = Address(street="", city="", zipcode="", valid=False)
        expected_result = list(partition(2, interleave([addresses, expected_verified_addresses])))
        self.assertEqual(verified_addresses, expected_result)


if __name__ == "__main__":
    main()
