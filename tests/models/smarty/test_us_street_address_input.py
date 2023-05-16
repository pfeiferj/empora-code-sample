from unittest import TestCase, main
from sample.models.smarty.us_street_address_input import USAddressInput

class TestUSAddressInput(TestCase):
    def test_is_valid_input_id(self):
        valid_address = USAddressInput(input_id="a"*36, street="")
        invalid_address = USAddressInput(input_id="a"*37, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_street(self):
        valid_address = USAddressInput(street="a"*50)
        invalid_address = USAddressInput(street="a"*51)
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_street2(self):
        valid_address = USAddressInput(street2="a"*50, street="")
        invalid_address = USAddressInput(street2="a"*51, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_secondary(self):
        valid_address = USAddressInput(secondary="a"*50, street="")
        invalid_address = USAddressInput(secondary="a"*51, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_city(self):
        valid_address = USAddressInput(city="a"*64, street="")
        invalid_address = USAddressInput(city="a"*65, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_state(self):
        valid_address = USAddressInput(state="a"*32, street="")
        invalid_address = USAddressInput(state="a"*33, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_zipcode(self):
        valid_address = USAddressInput(zipcode="a"*16, street="")
        invalid_address = USAddressInput(zipcode="a"*17, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_lastline(self):
        valid_address = USAddressInput(lastline="a"*64, street="")
        invalid_address = USAddressInput(lastline="a"*65, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_addressee(self):
        valid_address = USAddressInput(addressee="a"*64, street="")
        invalid_address = USAddressInput(addressee="a"*65, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_urbanization(self):
        valid_address = USAddressInput(urbanization="a"*64, street="")
        invalid_address = USAddressInput(urbanization="a"*65, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())

    def test_is_valid_match(self):
        valid_address = USAddressInput(match="a"*8, street="")
        invalid_address = USAddressInput(match="a"*9, street="")
        self.assertTrue(valid_address.is_valid())
        self.assertFalse(invalid_address.is_valid())



if __name__ == "__main__":
    main()
