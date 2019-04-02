import asyncpg
from gapsule import models


async def make_connect(config_info):
    try:
        con = await asyncpg.connect(user=config_info['dbuser'], database=config_info['dbname'])
    except asyncpg.InvalidCatalogNameError:
        print('err')
        con1 = await asyncpg.connect(user=config_info['dbuser'], database='postgres')
        await con1.execute('''CREATE DATABASE '''+config_info['dbname'])
        await con1.close()
        con = await asyncpg.connect(user=config_info['dbuser'], database=config_info['dbname'])
        await con.execute(
            '''CREATE TABLE users_info(
            UID SERIAL PRIMARY KEY,
            username  varchar(20) NOT NULL,
            mail_address varchar(40),
            password varchar(40) NOT NULL,
            salt char(10)
            );
            CREATE TABLE profiles(
            username   varchar(20) NOT NULL,
            icon_url   varchar(40),
            introduction    varchar(200)
            );
            CREATE TABLE log_info(
            username   varchar(20) NOT NULL,
            login_time  time NOT NULL,
            )
            '''
        )

    models.connection = con
