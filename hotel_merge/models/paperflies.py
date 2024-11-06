"""This module contains the models from ACME"""
from typing import List, Any, Union

from pydantic import BaseModel, Field, field_validator, model_serializer

from models.validators import parse_cooridinate


class ImageModel(BaseModel, str_strip_whitespace=True):
    link: str
    description: str = Field(alias="caption")

    def __str__(self):
        return '|'.join([self.description, self.link])


class ImagesField(BaseModel, str_strip_whitespace=True):
    rooms: List[ImageModel] = []
    site: List[ImageModel] = []

    @model_serializer
    def normalize(self):
        _temp_dict = {}
        for image in self.rooms:
            _temp_dict[str(image)] = image
        self.rooms = list(_temp_dict.values())

        _temp_dict = {}
        for image in self.site:
            _temp_dict[str(image)] = image
        self.site = list(_temp_dict.values())

        return dict(self)


class LocaltionModel(BaseModel, str_strip_whitespace=True):
    address: str
    country: str

    @field_validator('address', 'country', mode='before')
    @classmethod
    def parse(cls, v: Any) -> str:
        if v is None:
            return ''
        return str(v)


class AmenitiesField(BaseModel, str_strip_whitespace=True):
    general: List[str] = []
    room: List[str] = []


class PaperfliesHotel(BaseModel, str_strip_whitespace=True):
    id: str = Field(alias="hotel_id")
    destination_id: int
    name: str = Field(alias="hotel_name")
    description: str = Field(alias="details")
    location: LocaltionModel
    amenities: AmenitiesField
    images: ImagesField
    booking_conditions: List[str]

    @field_validator('description', mode='before')
    @classmethod
    def parse_description(cls, v: Any) -> str:
        if v is None:
            return ''
        return str(v)