import asyncpg
import passlib

from asyncpg import _testbase as tb

from auth.db import USERS_TABLE_NAME, init_db, _create_user, _get_user
from auth.user import User


async def count_rows(con: asyncpg.connect, table: str):
    r = await con.fetchrow(f'SELECT COUNT(*) FROM {table}')
    return r['count']


class TestDB(tb.ConnectedTestCase):

    async def test_create_user(self):
        await init_db(self.con)
        test_user = User('test', 'test1234')
        rows_len = await count_rows(self.con, USERS_TABLE_NAME)
        await _create_user(self.con, test_user)
        rows_len_after = await count_rows(self.con, USERS_TABLE_NAME)
        self.assertEqual(rows_len_after - rows_len, 1)

    async def test__get_user(self):
        await init_db(self.con)
        test_user = User('admin', 'admin')
        user = await _get_user(self.con, test_user.username)
        self.assertEqual(test_user.username, user.username)
        is_verified = passlib.hash.pbkdf2_sha256.verify(test_user.password, user.password)
        self.assertEqual(is_verified, True)
