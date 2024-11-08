import settings
import requests
from collections import defaultdict
from functools import lru_cache
from typing import Union, Optional, List
from models.acme import ACMEHotel
from models.patagonia import PatagoniaHotel
from models.paperflies import PaperfliesHotel
from models.hotel import Hotel
from helpers import import_class_by_path, ttl_hash


def get_hotels_by_supplier(url: str, kls: Union[ACMEHotel, PatagoniaHotel, PaperfliesHotel]) -> dict[Union[ACMEHotel, PatagoniaHotel, PaperfliesHotel]]:
    result = dict()
    response = requests.get(url)
    for hotel in response.json():
        item: Union[ACMEHotel, PatagoniaHotel, PaperfliesHotel] = kls(**hotel)
        if not item.id:
            continue
        result[item.id] = item
    return result


@lru_cache(maxsize=128)
def get_hotels_as_dicts(ttl: Optional[int] = None) -> tuple[dict[Hotel], dict[Hotel]]:
    """
    Retrieves and merges hotel data from multiple suppliers into a dictionary
    of Hotel objects. The results are cached for efficiency.

    :param ttl: Optional time-to-live parameter, used for cache from caller only.
    :type ttl: Optional[int]
    :return: A dictionary mapping hotel IDs to normalized hotel data.
    :rtype: dict[Hotel]
    """
    del ttl

    list_by_id: dict[Hotel] = dict()
    list_by_dest: dict[dict[Hotel]] = defaultdict(dict)
    for supplier, url in settings.ENDPOINTS.items():
        kls = import_class_by_path(settings.DATACLASSES[supplier])
        sup_hotels = get_hotels_by_supplier(url, kls)

        for h_id, h in sup_hotels.items():
            if h_id not in list_by_id:
                list_by_id[h_id] = Hotel()
            list_by_id[h_id].append_info(h)

    h: Hotel
    for h_id, h in list_by_id.items():
        h.normalize()
        list_by_dest[h.destination_id][h_id] = h
    return list_by_id, list_by_dest


def get_hotel_by_id(id: str) -> Optional[Hotel]:
    """
    Retrieves a single hotel by its ID from the cache.

    :param id: The hotel ID to retrieve.
    :type id: str
    :return: The hotel data if found, otherwise None.
    :rtype: Optional[Hotel]
    """
    hotels, _ = get_hotels_as_dicts(ttl_hash(settings.CACHE_TTL))
    return hotels.get(id)


def get_hotel_by_dest(dest_id: int) -> dict[dict[Hotel]]:
    """
    Retrieves a dictionary of hotels by their destination ID from the cache.

    :param dest_id: The destination ID to retrieve hotels for.
    :type dest_id: int
    :return: A dictionary mapping hotel IDs to Hotel objects for the specified 
             destination, or None if no hotels are found for the destination.
    :rtype: dict[dict[Hotel]]
    """
    _, hotels = get_hotels_as_dicts(ttl_hash(settings.CACHE_TTL))
    return hotels.get(dest_id)
