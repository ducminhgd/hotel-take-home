"""This module contains the models from ACME"""
from typing import List, Any, Union

from pydantic import BaseModel, Field, field_validator

from models.validators import parse_cooridinate


class ACMEHotel(BaseModel, str_strip_whitespace=True):
    id: str = Field(alias="Id")
    destination_id: int = Field(alias="DestinationId")
    name: str = Field(alias="Name")
    lat: Union[float, None] = Field(None, alias="Latitude")
    lng: Union[float, None] = Field(None, alias="Longitude")
    address: str = Field(alias="Address")
    city: str = Field(alias="City")
    country: str = Field(alias="Country")
    postal_code: str = Field(alias="PostalCode")
    description: str = Field(alias="Description")
    facilities: List[str] = Field(alias="Facilities")

    @field_validator('lat', 'lng', mode='before')
    @classmethod
    def parse_lat_lng(cls, v: Any) -> Union[float, None]:
        return parse_cooridinate(v)
