from aiohttp.web import Request, Response

from auth.functools import compose
from auth import logger
from auth import response


async def ping_handler(request: Request) -> Response:
    return compose(
        logger.debug,
        response.return_response)('"pong"')
