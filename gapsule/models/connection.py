import asyncpg
from gapsule import models


async def make_connect(config_info):
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

    models.connection = con
