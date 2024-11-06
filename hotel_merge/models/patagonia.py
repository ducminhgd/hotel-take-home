"""This module contains the models from ACME"""
from typing import List, Any, Union

from pydantic import BaseModel, Field, field_validator, model_serializer

from models.validators import parse_cooridinate


class ImageModel(BaseModel, str_strip_whitespace=True):
    link: str = Field(alias="url")
    description: str

    def __str__(self):
        return '|'.join([self.description, self.link])


class ImagesField(BaseModel, str_strip_whitespace=True):
    rooms: List[ImageModel] = []
    amenities: List[ImageModel] = []

    @model_serializer
    def normalize(self):
        _temp_dict = {}
        for image in self.rooms:
            _temp_dict[str(image)] = image
        self.rooms = list(_temp_dict.values())

        _temp_dict = {}
        for image in self.amenities:
            _temp_dict[str(image)] = image
        self.amenities = list(_temp_dict.values())

        return dict(self)


class PatagoniaHotel(BaseModel, str_strip_whitespace=True):
    id: str
    destination_id: int = Field(alias="destination")
    name: str
    lat: float | None
    lng: float | None
    address: str
    description: str = Field(alias="info")
    amenities: List[str]
    images: ImagesField

    @field_validator('lat', 'lng', mode='before')
    @classmethod
    def parse_lat_lng(cls, v: Any) -> Union[float, None]:
        return parse_cooridinate(v)

    @field_validator('address', mode='before')
    @classmethod
    def parse_address(cls, v: Any) -> str:
        if v is None:
            return ''
        return str(v)

    @field_validator('description', mode='before')
    @classmethod
    def parse_description(cls, v: Any) -> str:
        if v is None:
            return ''
        return str(v)

    @field_validator('amenities', mode='before')
    @classmethod
    def parse_amenities(cls, v: Any) -> str:
        if not isinstance(v, list):
            return []
        return v
