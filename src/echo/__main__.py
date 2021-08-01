import logging
import os
import socket
import sys
import typing as t

from aiohttp import web


async def handle_echo_request(request: web.Request) -> web.Response:
    return web.json_response(
        data={
            "hostname": socket.gethostname(),
            "method": request.method,
            "path": request.path,
            "headers": dict(request.headers),
            "body": (await request.json()) if request.body_exists else None,
        },
    )


async def handle_health_check(request: web.Request) -> web.Response:
    return web.json_response(
        data={
            "status": "OK",
        },
    )


def print_nothing(*args: t.Any, **kwargs: t.Any) -> None:
    pass


def main(args: t.Sequence[str]) -> int:
    logging.basicConfig(
        level=logging.DEBUG,
    )

    app = web.Application(
        middlewares=(
            web.normalize_path_middleware(),
        ),
    )

    app.router.add_route("*", "/", handle_echo_request)
    app.router.add_route("GET", "/health", handle_health_check)

    web.run_app(
        app=app,
        port=int(os.getenv("HTTP_PORT", 8080)),
        print=print_nothing,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
