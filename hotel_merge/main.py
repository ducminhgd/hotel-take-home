from sanic import Sanic, json
from sanic.request import Request

app = Sanic("Hotels")


@app.get("/")
async def hotels(request: Request):
    hotel_ids = request.args.get("hotels", default="").split(",")
    destination_id = request.args.get("destination", default=None)
        
    return json([])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
