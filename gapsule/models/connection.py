from gapsule import settings
import asyncio

import asyncpg


async def _make_connect_pool(config_info):
    try:
        pool = await asyncpg.create_pool(user=config_info['dbuser'],
                                         database=config_info['dbname'])
    except asyncpg.InvalidCatalogNameError:
        con1 = await asyncpg.connect(user=config_info['dbuser'],
                                     database='postgres')
        await con1.execute('''CREATE DATABASE ''' + config_info['dbname'])
        await con1.close()

        pool = await asyncpg.create_pool(user=config_info['dbuser'],
                                         database=config_info['dbname'])

        await pool.execute('''CREATE TABLE users_info(
            uid SERIAL,
            username  varchar(20) primary key,
            mail_address varchar,
            password varchar NOT NULL,
            salt varchar
            );
            CREATE TABLE profiles(
            username   varchar(20) references users_info(username) on delete cascade,
            icon_url   varchar(40),
            firstname   varchar not null,
            lastname    varchar not null,
            introduction    varchar,
            company     varchar,
            location    varchar,
            public_email    varchar,
            website     varchar
            );
            CREATE TABLE log_info(
            username   varchar(20) references users_info(username) on delete cascade,
            session     varchar,
            login_time  timestamptz
            );
            CREATE TABLE repos(
            repo_id     SERIAL,
            username    varchar(20) references users_info(username) on delete cascade,
            reponame    varchar,
            introduction    varchar,
            create_time     timestamptz,
            star_num    integer,
            fork_num    integer,
            visibility  boolean,
            forked_from     varchar,
            default_branch   varchar,
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
            is_issue    boolean,
            postername    varchar(20) references users_info(username) on delete cascade,
            title       varchar,
            status      varchar,
            visibility  boolean,
            post_time   timestamptz,
            primary key(repo_id,post_id)
            );
            CREATE TABLE comments(
            post_id     integer,
            repo_id     integer,
            comment_id  integer,
            is_reply    boolean,
            reply_to_id   integer,
            address_time  timestamptz,
            type        varchar,
            content   varchar,
            commenter varchar    references users_info(username) on delete cascade,
            primary key(repo_id,post_id,comment_id),
            foreign key (post_id, repo_id) references posts(post_id, repo_id)
            );
            CREATE TABLE notifications(
            username   varchar(20) references users_info(username) on delete cascade,
            notification_id     integer,
            created_time    timestamptz,
            content         varchar,
            primary key(username,notification_id)
            );
            CREATE TABLE pull_requests(
            dest_repo_id     integer,
            dest_branch     varchar,
            pull_id          integer,
            src_repo_id     integer,
            src_branch      varchar,
            created_time    timestamptz,
            status          varchar,
            auto_merge_status   varchar,
            primary key(dest_repo_id,pull_id)
            );
            ''')

    return pool


def _create_instance():
    try:
        tmp_loop = asyncio.get_event_loop()
        pool = tmp_loop.run_until_complete(
            _make_connect_pool(settings.settings))
        return pool
    except Exception as e:
        raise RuntimeError("Database connection initiation failed.") from e


_connection = _create_instance()


async def fetchrow(*args):
    global _connection
    return await _connection.fetchrow(*args)


async def fetch(*args):
    global _connection
    return await _connection.fetch(*args)


async def execute(*args):
    global _connection
    return await _connection.execute(*args)
