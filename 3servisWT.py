from aiohttp import web
from OuterFunc import ForwardToService4

responses = []

routes = web.RouteTableDef()

@routes.post("/")
async def second_service(request):
    global responses
    try:
        data = await request.json()  # data is a list of dictionaries
        for item in data:
            username = item["username"]
            content = item["content"]
            if username.lower().startswith("d"):
                response = await ForwardToService4(item)  # Pass the whole dictionary
                print(response)
                responses.append(response)
        return web.json_response(
            {"name": "Service 2", "status": "OK", "Service 4 response": responses},
            status=200,
        )
    except Exception as e:
        return web.json_response({"name": "Service 2", "error": str(e)}, status=500)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8083)