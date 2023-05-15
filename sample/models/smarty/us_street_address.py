from typing import Optional
from pydantic import (BaseModel)
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


class USAddressComponents(BaseModel):
    """
    The individual parts of an address as returned by smarty.
    """

    urbanization: str = ""
    street_name: str = ""
    street_predirection: str = ""
    street_postdirection: str = ""
    street_suffix: str = ""
    primary_number: str = ""
    secondary_number: str = ""
    secondary_designator: str = ""
    extra_secondary_number: str = ""
    extra_secondary_designator: str = ""
    pmb_designator: str = ""
    pmb_number: str = ""
    city_name: str = ""
    default_city_name: str = ""
    state_abbreviation: str = ""
    zipcode: str = ""
    plus4_code: str = ""
    delivery_point: str = ""
    delivery_point_check_digit: str = ""


class USAddressMetadata(BaseModel):
    """
    Additional address information from the usps.
    """

    record_type: str = ""
    zip_type: str = ""
    county_fips: str = ""
    county_name: str = ""
    ews_match: str = ""
    carrier_route: str = ""
    congressional_district: str = ""
    building_default_indicator: str = ""
    rdi: str = ""
    elot_sequence: str = ""
    elot_sort: str = ""
    latitude: str = ""
    longitude: str = ""
    coordinate_license: str = ""
    precision: str = ""
    time_zone: str = ""
    utc_offset: str = ""
    dst: str = ""


class USAddressAnalysis(BaseModel):
    """
    Information about the address analysis from smarty.
    """

    dpv_match_code: str = ""
    dpv_footnotes: str = ""
    dpv_cmra: str = ""
    dpv_vacant: str = ""
    dpv_no_stat: str = ""
    active: str = ""
    footnotes: str = ""
    lacslink_code: str = ""
    lacslink_indicator: str = ""
    suitelink_match: str = ""
    enhanced_match: str = ""


class USAddressOutput(BaseModel):
    """
    An output model from the smarty US Street Address API.
    """

    input_id: str = ""
    input_index: int = 0
    candidate_index: int = 0
    addressee: str = ""
    delivery_line_1: str = ""
    delivery_line_2: str = ""
    last_line: str = ""
    delivery_point_barcode: str = ""
    components: USAddressComponents = USAddressComponents()
    metadata: USAddressMetadata = USAddressMetadata()
    analysis: USAddressAnalysis = USAddressAnalysis()

    def to_address(self) -> Address:
        # Get each part of the internal address model
        street = self.get_street()
        city = self.get_city()
        zipcode = self.get_zipcode()
        valid = self.is_valid()

        return Address(street=street, city=city, zipcode=zipcode, valid=valid)

    def get_street(self) -> str:
        """
        Retrieve the street address from a smarty address response.
        """

        c = self.components

        # Build street from components excluding optional parts if missing
        street = c.primary_number
        if c.street_predirection != "":
            street += f" {c.street_predirection}"
        street += f" {c.street_name}"
        if c.street_suffix != "":
            street += f" {c.street_suffix}"

        return street

    def is_valid(self) -> bool:
        """
        Checks a smarty_address response to see if the address is in the usps database.
        """
        # validation field
        match_code = self.analysis.dpv_match_code

        # valid if address is in usps database
        valid = match_code in ["Y", "S", "D"]

        return valid

    def get_zipcode(self) -> str:
        """
        Retrieve the zipcode from a smarty address response.
        """
        zipcode = self.components.zipcode

        # add plus4 if it exists
        if self.components.plus4_code != "":
            zipcode += f"-{self.components.plus4_code}"

        return zipcode

    def get_city(self) -> str:
        """
        Retrieve the city from a smarty address response.
        """
        return self.components.city_name
