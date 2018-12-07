from aiohttp.web import Request, Response, json_response

from auth import logger
from auth.db import create_user
from auth.functools import compose
from auth.token import create_token
from auth.typing import Maybe, Error, Success
from auth.verify import check_password


async def auth_handler(request: Request) -> Response:
    return await compose(
        check_password,
        logger.debug,
        create_token,
        logger.debug,
        return_response
    )(request)


async def create_user_handler(request: Request) -> Response:
    return await compose(
        create_user,
        return_response
    )(request)


def return_response(r: Maybe[Success]) -> Response:
    if isinstance(r, Error):
        return json_response(r.msg, status=r.status_code)
    return json_response(r.json, status=r.status_code)
