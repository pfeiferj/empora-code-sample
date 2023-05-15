from unittest import TestCase, main
from sample.models.address import Address

class TestAddress(TestCase):
    def test_address_strips_leading_trailing_spaces(self):
        addr = Address(street="  123 Main St  ", city="Columbus  ", zipcode="  43215")

        self.assertEqual(addr.street, "123 Main St")
        self.assertEqual(addr.city, "Columbus")
        self.assertEqual(addr.zipcode, "43215")

    def test_address_format(self):
        addr = Address(street="  123 Main St  ", city="Columbus  ", zipcode="  43215")

        self.assertEqual(addr.format(), "123 Main St, Columbus, 43215")

    def test_address_is_header(self):
        addr = Address(street="Street", city="City", zipcode="zip code")

        self.assertTrue(addr.is_header())

    def test_address_is_not_header(self):
        addr = Address(street="  123 Main St  ", city="Columbus  ", zipcode="  43215")

        self.assertFalse(addr.is_header())


if __name__ == '__main__':
    main()
