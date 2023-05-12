from typing import Optional
from pydantic import (
    BaseModel,
)


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
