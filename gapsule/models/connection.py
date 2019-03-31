import asyncpg
from gapsule import models


async def make_connect(config_info):
    try:
        con = await asyncpg.connect(user=config_info['dbuser'], database=config_info['dbname'])
    except asyncpg.InvalidCatalogNameError:
        con1 = await asyncpg.connect(user=config_info['dbuser'])
        await con1.execute('''create database '''+config_info['dbname']+''';''')
        await con1.close()
        con = await asyncpg.connect(user=config_info['dbuser'], database=config_info['dbname'])
        await con.execute(
            '''CREATE TABLE users_info(
            UID SERIAL PRIMARY KEY,
            username  varchar(20),
            mail_address varchar(40),
            password varchar(40)
            )'''
        )

    models.connection = con
