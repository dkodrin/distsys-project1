import pathlib
import aiofiles
from aiohttp import web

Code = []

routes = web.RouteTableDef()

@routes.post("/gatherData")
async def fourth_service(request):
	global Code
	try:
		data = await request.json()
		Code.append({"username": data.get("username"), "content": data.get("content")})
		if len(Code) > 10:
			pathlib.Path("files").mkdir(parents = True, exist_ok = True)
			for item in Code:
				async with aiofiles.open("files/%s.txt"%(item.get("username")), "w") as writer:
					await writer.write(item.get("content"))
			Code.clear()
		return web.json_response({"name": "Service 4", "status": "OK"}, status = 200)
	except Exception as e:
		return web.json_response({"name": "Service 4", "error": str(e)}, status = 500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8084)