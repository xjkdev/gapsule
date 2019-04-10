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
            uid SERIAL,
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
            CREATE TABLE repos(
            repo_id     SERIAL,
            username    varchar(20) references users_info(username),
            reponame    varchar,
            introduction    varchar,
            create_time     TIMESTAMP,
            star_num    integer,
            fork_num    integer,
            visibility  boolean,
            primary key(username,reponame)
            );
            CREATE TABLE collaborate(
            repo_id     integer,
            collaborator    varchar
            );
            CREATE TABLE read_permission(
            repo_id     integer,
            username    varchar
            );
            CREATE TABLE admin_permission(
            repo_id     integer,
            username   varchar
            );
            CREATE TABLE posts(
            post_id    integer ,
            repo_id    integer ,
            postername    varchar(20) references users_info(username),
            title       varchar,
            status      varchar,
            visibility  boolean,
            post_time   timestamp,
            primary key(repo_id,post_id)
            );

            CREATE TABLE comments(
            post_id     integer,
            repo_id     integer,
            comment_id  integer,
            is_reply    boolean,
            reply_to    varchar(20)  references users_info(username),
            address_time  timestamp,
            type        varchar,
            content   varchar,
            conmmenter varchar    references users_info(username),
            primary key(repo_id,post_id,comment_id),
            foreign key (post_id, repo_id) references posts(post_id, repo_id)
            )
            '''
        )
    return con


def _create_instance():
    try:
        tmp_loop = asyncio.get_event_loop()
        conn = tmp_loop.run_until_complete(_make_connect(settings.settings))
        return conn
    except Exception as e:
        raise RuntimeError("Database connection initiation failed.") from e


_connection = _create_instance()

fetch = _connection.fetch
fetchrow = _connection.fetchrow
execute = _connection.execute
