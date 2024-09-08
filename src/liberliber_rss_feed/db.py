from contextlib import contextmanager
from sqlite3 import PARSE_DECLTYPES
from sqlite3 import Connection
from sqlite3 import connect
from sqlite3 import register_converter
from typing import TYPE_CHECKING
from typing import NamedTuple

from .dt import from_timestamp

if TYPE_CHECKING:
    from collections.abc import Iterator
    from datetime import datetime

    from .config import Config

register_converter('timestamp', from_timestamp)


def create_schema(connection: Connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
            create table if not exists rss_items(
                guid TEXT primary key,
                title TEXT,
                link TEXT,
                description TEXT,
                creation_date timestamp default current_timestamp,
                published_date timestamp
            )
            """
    )
    connection.commit()


class RowNotFoundError(Exception): ...


class RssItem(NamedTuple):
    guid: str
    title: str
    link: str
    description: str


class FullRssItem(NamedTuple):
    guid: str
    title: str
    link: str
    description: str
    creation_date: 'datetime'
    published_date: 'datetime'


class Db:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def upsert(self, rss_item: RssItem) -> int | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            insert into rss_items(guid, title, link, description)
            values (?,?,?,?)
            on conflict(guid) do update set title=?, link=?, description=?
            """,
            (
                rss_item.guid,
                rss_item.title,
                rss_item.link,
                rss_item.description,
                rss_item.title,
                rss_item.link,
                rss_item.description,
            ),
        )
        self.connection.commit()
        return cursor.lastrowid

    def select_first_unpublished(self) -> RssItem:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            select guid, title, link, description
            from rss_items
            where published_date is null
            order by creation_date
            """
        )
        row = cursor.fetchone()
        if row is None:
            raise RowNotFoundError
        return RssItem(*row)

    def update_publish(self, guid: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            update rss_items set published_date=current_timestamp
            where guid=?
            """,
            (guid,),
        )
        self.connection.commit()

    def update_unpublish(self, guid: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            update rss_items set published_date=null
            where guid=?
            """,
            (guid,),
        )
        self.connection.commit()

    def full_rss_items(self) -> 'Iterator[FullRssItem]':
        cursor = self.connection.cursor()
        cursor.execute(
            """
            select guid, title, link, description, creation_date, published_date
            from rss_items
            order by creation_date
            """
        )
        for row in cursor.fetchall():
            yield FullRssItem(*row)


@contextmanager
def db_connection(config: 'Config') -> 'Iterator[Db]':
    connection = connect(
        config['sqlfn'], detect_types=PARSE_DECLTYPES, check_same_thread=False
    )
    try:
        create_schema(connection)
        yield Db(connection)
    finally:
        connection.close()
