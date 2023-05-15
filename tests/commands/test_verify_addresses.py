from unittest import TestCase, main
from unittest.mock import patch, call
from functools import wraps
from tests.data.addresses import basic_address_list, basic_address_csv
import os


def mock_decorator(*args, **kwargs):
    """Decorate by doing nothing."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# PATCH THE DECORATOR HERE
patch("click.command", mock_decorator).start()
patch("click.argument", mock_decorator).start()

from sample.commands.verify_addresses import verify_addresses  # noqa: E402 Purposefully imported after patching click

dir_path = os.path.dirname(os.path.realpath(__file__))


stdin_patch = basic_address_csv()
stdin_patch.fileno = lambda: 0


class TestVerifyAddresses(TestCase):
    @patch("os.isatty", return_value=True)
    @patch("sample.actions.verify_addresses.verify_addresses", return_value=basic_address_list())
    @patch("builtins.print")
    def test_verify_addresses(self, mock_print, mock_verify_addresses, mock_isatty):
        verify_addresses(basic_address_csv())
        mock_print.assert_has_calls(
            [
                call("143 e Maine Street, Columbus, 43215 -> 143 E Main St, Columbus, 43215-5370"),
                call("1 Empora St, Title, 11111 -> Invalid Address"),
            ]
        )

    @patch("sys.stdin", stdin_patch)
    @patch("os.isatty", return_value=False)
    @patch("sample.actions.verify_addresses.verify_addresses", return_value=basic_address_list())
    @patch("builtins.print")
    def test_verify_addresses_stdin(self, mock_print, mock_verify_addresses, mock_isatty):
        verify_addresses(basic_address_csv())
        mock_print.assert_has_calls(
            [
                call("143 e Maine Street, Columbus, 43215 -> 143 E Main St, Columbus, 43215-5370"),
                call("1 Empora St, Title, 11111 -> Invalid Address"),
            ]
        )

    @patch("os.isatty", return_value=True)
    @patch("sample.actions.verify_addresses.verify_addresses", return_value=basic_address_list())
    @patch("builtins.print")
    def test_verify_addresses_no_file(self, mock_print, mock_verify_addresses, mock_isatty):
        with self.assertRaises(Exception) as cm:
            verify_addresses(None)

        exception = cm.exception
        self.assertEqual(
            str(exception),
            "No file provided.\n"
            "Please pass the file name as the first argument or pipe the file data to this command.\n",
        )


if __name__ == "__main__":
    main()
