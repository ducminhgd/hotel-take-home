from sanic import Sanic, json
from sanic.request import Request

from repository import get_hotel_by_id, get_hotel_by_dest

app = Sanic("Hotels")


@app.get("/")
async def hotels(request: Request):
    hotel_ids: list[str] = request.args.get("hotels", default="").split(",")
    destination_id: str = request.args.get("destination", default=None)

    d_result = {}

    if destination_id:
        destination_id = int(destination_id)
        d_result = get_hotel_by_dest(destination_id)

    for id in hotel_ids:
        hotel = get_hotel_by_id(id.strip())
        if not hotel or hotel.id in d_result:
            continue
        d_result[id] = hotel

    if not d_result:
        return json([])
    result = []
    for k, v in d_result.items():
        result.append(v.model_dump())
    return json(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
