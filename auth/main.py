import aiohttp.web

from auth.app import get_app
from auth.logger import access_logger


def main():
    app = get_app()
    aiohttp.web.run_app(app, access_log=access_logger)
