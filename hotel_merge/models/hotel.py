"""This module is the model for our system Hotel
"""
from typing import List

from pydantic import BaseModel, model_serializer, Field
from models.acme import ACMEHotel
from models.patagonia import PatagoniaHotel
from models.paperflies import PaperfliesHotel
from helpers import remove_duplicates, method_dispatch


class LocationField(BaseModel, str_strip_whitespace=True):
    lat: float | None = None
    lng: float | None = None
    address: str = ''
    city: str = ''
    country: str = ''


class AmenitiesField(BaseModel, str_strip_whitespace=True):
    general: List[str] = []
    room: List[str] = []

    @model_serializer
    def normalize(self):
        self.general = remove_duplicates(self.general)
        self.room = remove_duplicates(self.room)
        return dict(self)


class ImageModel(BaseModel, str_strip_whitespace=True):
    link: str
    description: str

    def __str__(self):
        return '|'.join([self.description, self.link])


class ImagesField(BaseModel, str_strip_whitespace=True):
    rooms: List[ImageModel] = []
    site: List[ImageModel] = []
    amenities: List[ImageModel] = []

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

        _temp_dict = {}
        for image in self.amenities:
            _temp_dict[str(image)] = image
        self.amenities = list(_temp_dict.values())

        return dict(self)


class Hotel(BaseModel, str_strip_whitespace=True):
    id: str = Field('')
    destination_id: int = Field(0)
    name: str = ''
    location: LocationField = Field(default_factory=LocationField)
    description: str = ''
    amenities: AmenitiesField = Field(default_factory=AmenitiesField)
    images: ImagesField = Field(default_factory=ImagesField)
    booking_conditions: List[str] = Field(default_factory=list)

    @model_serializer
    def normalize(self):
        self.amenities.normalize()
        self.images.normalize()
        self.booking_conditions = remove_duplicates(self.booking_conditions)
        return dict(self)

    @method_dispatch
    def append_info(self, obj):
        raise NotImplementedError(f'Not implemented for {
                                  obj.__class__.__name__}')

    @append_info.register(ACMEHotel)
    def _append_info_acme(self, obj: ACMEHotel):
        self.id = obj.id
        self.destination_id = obj.destination_id
        self.name = obj.name
        self.description = obj.description

        self.location.lat = obj.lat
        self.location.lng = obj.lng
        self.location.address = obj.address
        self.location.city = obj.city
        self.location.country = obj.country

        self.amenities.general.extend(obj.facilities)

    @append_info.register(PatagoniaHotel)
    def _append_info_patagonia(self, obj: PatagoniaHotel):
        self.id = obj.id
        self.destination_id = obj.destination_id
        self.name = obj.name
        self.description = obj.description

        self.location.lat = obj.lat
        self.location.lng = obj.lng

        self.amenities.general.extend(obj.amenities)
        for image in obj.images.rooms:
            self.images.rooms.append(ImageModel(**image.__dict__))
        for image in obj.images.amenities:
            self.images.amenities.append(ImageModel(**image.__dict__))

    @append_info.register(PaperfliesHotel)
    def _append_info_paperflies(self, obj: PaperfliesHotel):
        self.id = obj.id
        self.destination_id = obj.destination_id
        self.name = obj.name
        self.description = obj.description

        self.location.address = obj.location.address
        self.location.country = obj.location.country

        self.amenities.general.extend(obj.amenities.general)
        self.amenities.room.extend(obj.amenities.room)
        for image in obj.images.rooms:
            self.images.rooms.append(ImageModel(**image.__dict__))
        for image in obj.images.site:
            self.images.site.append(ImageModel(**image.__dict__))

        self.booking_conditions.extend(obj.booking_conditions)
