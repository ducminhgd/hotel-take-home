from typing import Any, Union

def parse_cooridinate(lat_or_long: Any) -> Union[float, None]:
    if lat_or_long is None:
        return None
    if isinstance(lat_or_long, str) and lat_or_long=='':
        return None
    return float(lat_or_long)