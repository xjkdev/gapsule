import asyncio

import asyncpg
from gapsule import settings


async def _make_connect(config_info):
    try:
        con = await asyncpg.connect(user=config_info['dbuser'], database=config_info['dbname'])
    except asyncpg.InvalidCatalogNameError:
        con1 = await asyncpg.connect(user=config_info['dbuser'], database='postgres')
        await con1.execute('''CREATE DATABASE '''+config_info['dbname'])
        await con1.close()
        con = await asyncpg.connect(user=config_info['dbuser'], database=config_info['dbname'])
        await con.execute(
            '''CREATE TABLE users_info(
            UID SERIAL,
            username  varchar(20) primary key,
            mail_address varchar(40),
            password varchar(40) NOT NULL,
            salt char(10)
            );
            CREATE TABLE profiles(
            username   varchar(20) references users_info(username),
            icon_url   varchar(40),
            introduction    varchar,
            company     varchar,
            location    varchar,
            website     varchar
            );
            CREATE TABLE log_info(
            username   varchar(20) references users_info(username),
            session     varchar,
            login_time  TIMESTAMP
            );
            '''
        )
    return con


def _create_instance():
    try:
        tmp_loop = asyncio.new_event_loop()
        conn = tmp_loop.run_until_complete(_make_connect(settings.settings))
        tmp_loop.close()
        return conn
    except Exception as e:
        raise RuntimeError("Database connection initiation failed.") from e


_connection = _create_instance()

fetchrow = _connection.fetchrow
execute = _connection.execute
