from sanic import Sanic, json
from sanic.request import Request

from repository import get_hotel_by_id, get_hotel_by_dest

app = Sanic("Hotels")


@app.get("/")
async def hotels(request: Request):
    hotel_ids: list[str] = request.args.get("hotels", default="").split(",")
    destination_id: str = request.args.get("destination", default=None)

    result = {}
    for id in hotel_ids:
        hotel = get_hotel_by_id(id.strip())
        if not hotel or hotel.id in result:
            continue
        result[id] = hotel.model_dump()

    if destination_id:
        try:
            destination_id = int(destination_id)
            hotel = get_hotel_by_dest(destination_id)
            if hotel and hotel.id not in result:
                result[hotel.id] = hotel.model_dump()
        except (ValueError, TypeError):
            destination_id = None

    if not result:
        return json([])
    return json(list(result.values()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
