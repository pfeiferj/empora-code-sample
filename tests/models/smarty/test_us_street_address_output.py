from unittest import TestCase, main
from sample.models.address import Address
from sample.models.smarty.us_street_address_output import USAddressOutput


class TestUSAddressOutput(TestCase):
    def test_to_address(self):
        data = USAddressOutput.parse_obj(
            {
                "components": {
                    "primary_number": "143",
                    "street_predirection": "E",
                    "street_name": "Main",
                    "street_suffix": "St",
                    "zipcode": "11111",
                    "plus4_code": "2222",
                    "city_name": "Columbus",
                },
                "analysis": {"dpv_match_code": "Y"},
            }
        )

        expected_response = Address(street="143 E Main St", city="Columbus", zipcode="11111-2222")

        self.assertEqual(data.to_address(), expected_response)

    def test_get_zipcode(self):
        data = USAddressOutput.parse_obj({"components": {"zipcode": "11111", "plus4_code": "2222"}})

        self.assertEqual(data.get_zipcode(), "11111-2222")

    def test_get_zipcode_no_plus_4(self):
        data = USAddressOutput.parse_obj({"components": {"zipcode": "11111"}})
        self.assertEqual(data.get_zipcode(), "11111")

    def test_get_street(self):
        data = USAddressOutput.parse_obj(
            {
                "components": {
                    "primary_number": "143",
                    "street_predirection": "E",
                    "street_name": "Main",
                    "street_suffix": "St",
                }
            }
        )
        self.assertEqual(data.get_street(), "143 E Main St")

    def test_get_street_no_predirection(self):
        data = USAddressOutput.parse_obj(
            {
                "components": {
                    "primary_number": "143",
                    "street_name": "Main",
                    "street_suffix": "St",
                }
            }
        )
        self.assertEqual(data.get_street(), "143 Main St")

    def test_get_street_no_suffix(self):
        data = USAddressOutput.parse_obj(
            {
                "components": {
                    "primary_number": "143",
                    "street_name": "Main",
                }
            }
        )
        self.assertEqual(data.get_street(), "143 Main")

    def test_get_city(self):
        data = USAddressOutput.parse_obj(
            {
                "components": {
                    "city_name": "Columbus",
                }
            }
        )
        self.assertEqual(data.get_city(), "Columbus")

    def test_is_valid(self):
        data = USAddressOutput.parse_obj(
            {
                "analysis": {
                    "dpv_match_code": "Y",
                }
            }
        )
        valid = data.is_valid()
        self.assertTrue(valid)

    def test_is_valid_not_in_usps(self):
        data = USAddressOutput.parse_obj(
            {
                "analysis": {
                    "dpv_match_code": "",
                }
            }
        )
        valid = data.is_valid()
        self.assertFalse(valid)

    def test_is_valid_ignored_secondary(self):
        data = USAddressOutput.parse_obj(
            {
                "analysis": {
                    "dpv_match_code": "S",
                }
            }
        )
        valid = data.is_valid()
        self.assertTrue(valid)

    def test_is_valid_missing_secondary(self):
        data = USAddressOutput.parse_obj(
            {
                "analysis": {
                    "dpv_match_code": "D",
                }
            }
        )
        valid = data.is_valid()
        self.assertTrue(valid)


if __name__ == "__main__":
    main()
