import aiohttp.web

from auth.db import setup_db
from auth.handlers import auth_handler, create_user_handler
from auth.ping import ping_handler
from auth.mq import init_rabbit_client


def get_app() -> aiohttp.web.Application:
    app = aiohttp.web.Application()
    app.on_startup.append(setup_db)
    app.on_startup.append(init_rabbit_client)
    app.add_routes([
        aiohttp.web.get('/ping', ping_handler),
        aiohttp.web.post('/auth', auth_handler),
        aiohttp.web.post('/user', create_user_handler),
    ])

    return app
