from pydantic import (
    BaseModel,
    validator,
)


class Address(BaseModel):
    """
    Address CSV row data model.
    """

    street: str
    city: str
    zipcode: str
    valid: bool = True

    @validator("street", "city", "zipcode")
    def remove_padding(cls, v: str):
        """
        Strips leading and trailing spaces from the value upon creation.
        """

        return v.lstrip(" ").rstrip(" ")

    def format(self) -> str:
        """
        Formats the address for display in the following format: street, city, zipcode
        """
        if self.valid:
            return f"{self.street}, {self.city}, {self.zipcode}"
        else:
            return "Invalid Address"

    def is_header(self) -> bool:
        """
        Checks if the address is a header row.
        """
        if self.street.lower() == "street" and self.city.lower() == "city" and self.zipcode.lower() == "zip code":
            return True

        return False
