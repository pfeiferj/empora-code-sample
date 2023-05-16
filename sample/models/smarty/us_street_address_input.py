from typing import Optional
from pydantic import BaseModel
from sample.models.address import Address


class USAddressInput(BaseModel):
    """
    An input model for the smarty US Street Address API.
    """

    input_id: Optional[str] = None
    street: str
    street2: Optional[str] = None
    secondary: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    lastline: Optional[str] = None
    addressee: Optional[str] = None
    urbanization: Optional[str] = None
    candidates: Optional[int] = None
    match: Optional[str] = None

    def is_valid(self) -> bool:
        """
        Validate whether fields meet smarty api requirements.
        """
        if self.input_id is not None and len(self.input_id) > 36:
            return False

        if len(self.street) > 50:
            return False

        if self.street2 is not None and len(self.street2) > 50:
            return False

        if self.secondary is not None and len(self.secondary) > 50:
            return False

        if self.city is not None and len(self.city) > 64:
            return False

        if self.state is not None and len(self.state) > 32:
            return False

        if self.zipcode is not None and len(self.zipcode) > 16:
            return False

        if self.lastline is not None and len(self.lastline) > 64:
            return False

        if self.addressee is not None and len(self.addressee) > 64:
            return False

        if self.urbanization is not None and len(self.urbanization) > 64:
            return False

        if self.match is not None and len(self.match) > 8:
            return False

        return True

    @staticmethod
    def from_address(address: Address, **kwargs):
        """
        Create a smarty input address from an internal Address representation
        """
        # Handle two line streets
        split_street = address.street.split("\n")
        street = split_street[0]
        street2: Optional[str] = None
        if len(split_street) == 2:
            street2 = split_street[1]
        if len(split_street) > 2:
            raise Exception("Street can only have up to two lines.")

        return USAddressInput(**kwargs, street=street, street2=street2, city=address.city, zipcode=address.zipcode)
