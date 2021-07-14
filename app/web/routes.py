from aiohttp import web


async def handler(request: web.Request):
    print(request.headers)
    return web.Response(text="Hello")


def register(app: web.Application):
    app.add_routes(
        [
            web.get("/", handler),
        ]
    )
