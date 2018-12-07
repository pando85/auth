import aiohttp
import asyncpg
import passlib.hash

from auth.config import (ADMIN_USER, ADMIN_PASSWORD, POSTGRES_HOST, POSTGRES_PORT,
                         POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
from auth import logger
from auth.user import User, to_dict
from auth.typing import Maybe, Error, Success

USERS_TABLE_NAME = 'users'


async def _check_table_exists(conn: asyncpg.connect, table: str) -> bool:
    r = await conn.fetchrow(f'''
        SELECT EXISTS (
            SELECT 1
            FROM   pg_tables
            WHERE  schemaname = 'public'
            AND    tablename = $1
            );
    ''', table)
    return r['exists']


async def _create_user(conn: asyncpg.connect, user: User) -> Maybe[User]:
    try:
        await conn.execute(f'''
            INSERT INTO {USERS_TABLE_NAME}(username, password) VALUES($1, $2)
        ''', user.username, passlib.hash.pbkdf2_sha256.hash(user.password))
    except asyncpg.exceptions.UniqueViolationError:
        return Error("'user already exists'", 409)
    return user


async def _update_user(conn: asyncpg.connect, user: User) -> Maybe[User]:
    await conn.execute(f'''
        UPDATE {USERS_TABLE_NAME} SET password = $2 WHERE username = $1
    ''', user.username, passlib.hash.pbkdf2_sha256.hash(user.password))
    return user


async def _get_user(conn: asyncpg.connection, username: str) -> Maybe[User]:
    row = await conn.fetchrow(
        f'SELECT * FROM {USERS_TABLE_NAME} WHERE username = $1', username)

    if not row:
        return Error("'user does not exists'", 422)
    return User(**dict(row))


async def init_db(conn: asyncpg.connect) -> None:
    if await _check_table_exists(conn, USERS_TABLE_NAME):
        logger.info('Already initializated.')
        return

    logger.info(f'Create table: {USERS_TABLE_NAME}')
    await conn.execute(f'''
        CREATE TABLE {USERS_TABLE_NAME}(
            username text PRIMARY KEY,
            password text
        )
    ''')

    logger.info(f'Create admin user')
    await _create_user(conn, User(ADMIN_USER, ADMIN_PASSWORD))


async def setup_db(app: aiohttp.web.Application) -> None:
    app['pool'] = await asyncpg.create_pool(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    async with app['pool'].acquire() as connection:
        await init_db(connection)


async def create_user(request: aiohttp.web.Request) -> Maybe[Success]:
    pool = request.app['pool']
    user_request = User(**(await request.json()))

    async with pool.acquire() as connection:
        maybe_user = await _create_user(connection, user_request)
        if isinstance(maybe_user, User):
            return Success(to_dict(maybe_user), 201)
        maybe_user = await _update_user(connection, user_request)
        if isinstance(maybe_user, User):
            return Success(to_dict(maybe_user), 200)
    return maybe_user


async def get_user(request: aiohttp.web.Request) -> Maybe[User]:
    pool = request.app['pool']
    user_request = User(**(await request.json()))

    async with pool.acquire() as connection:
        user = await _get_user(connection, user_request.username)
    return user
