# -*- coding: utf-8 -*-


from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException as StarletteHTTPException


class BaseRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            ip = (
                request.headers["x-forwarded-for"]
                if "x-forwarded-for" in request.headers.keys()
                else request.client.host
            )
            request.state.ip = ip.split(",")[0]
            try:
                response: Response = await original_route_handler(request)
            except Exception as e:
                # body = await request.body()
                if isinstance(e, StarletteHTTPException):
                    raise e

            return response

        return custom_route_handler
