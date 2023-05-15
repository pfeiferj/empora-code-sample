from io import StringIO
from unittest import TestCase, main
from sample.models.address import Address
from sample.actions.parse_addresses_csv import parse_addresses_csv


class TestParseAddressesCsv(TestCase):
    def test_parse_addresses_csv(self):
        csv = "143 E Main St,Columbus,43215\n1 Empora St,Title,11111"
        expected = [
            Address(street="143 E Main St", city="Columbus", zipcode="43215"),
            Address(street="1 Empora St", city="Title", zipcode="11111"),
        ]
        self.assertEqual(parse_addresses_csv(StringIO(csv)), expected)

    def test_parse_addresses_csv_invalid_row(self):
        csv = "143 E Main St,Columbus,43215,blah\n1 Empora St,Title,11111"

        with self.assertRaises(Exception) as cm:
            parse_addresses_csv(StringIO(csv))
        exception = cm.exception
        self.assertEqual(str(exception), "Invalid address row on line number: 1.")

    def test_parse_addresses_csv_no_addresses(self):
        csv = ""

        with self.assertRaises(Exception) as cm:
            parse_addresses_csv(StringIO(csv))
        exception = cm.exception
        self.assertEqual(str(exception), "No addresses found in file.")

    def test_parse_addresses_csv_strips_header(self):
        csv = "Street,City,Zip Code\n143 E Main St,Columbus,43215\n1 Empora St,Title,11111"
        expected = [
            Address(street="143 E Main St", city="Columbus", zipcode="43215"),
            Address(street="1 Empora St", city="Title", zipcode="11111"),
        ]
        self.assertEqual(parse_addresses_csv(StringIO(csv)), expected)


if __name__ == "__main__":
    main()
