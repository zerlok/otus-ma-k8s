import json
import logging
import os
import socket
import sys
import typing as t

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel, HttpUrl

router = APIRouter()


class DebugResponse(BaseModel):
    hostname: str
    method: str
    url: HttpUrl
    headers: t.Mapping[str, str]
    # FIXME: swagger displays type `string`
    body: t.Any


class HealthCheckResponse(BaseModel):
    status: str


if os.getenv("DEBUG", "false").lower() in {"1", "yes", "true"}:
    # FIXME: handler may receive one optional parameter
    @router.api_route("/", response_model=DebugResponse)
    async def handle_debug_request(request: Request) -> DebugResponse:
        body = await request.body()
        return DebugResponse(
            hostname=socket.gethostname(),
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers),
            body=json.loads(body) if body else None,
        )


@router.get("/health")
async def handle_health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="OK")


def main(args: t.Sequence[str]) -> int:
    logging.basicConfig(
        level=logging.DEBUG,
    )

    app = FastAPI()
    app.include_router(router)

    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("HTTP_PORT", 8000)))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
