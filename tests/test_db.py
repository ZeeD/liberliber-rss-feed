from unittest import TestCase

from _support.factories import c
from liberliber_rss_feed.db import RowNotFoundError
from liberliber_rss_feed.db import RssItem
from liberliber_rss_feed.db import db_connection


class TestDb(TestCase):
    def test_empty(self) -> None:
        with db_connection(c(sqlfn=':memory:')) as db:
            db.upsert(RssItem('foo', 'bar', 'baz', 'qux'))

            rss_item = db.select_first_unpublished()
            self.assertEqual(rss_item.guid, 'foo')
            self.assertEqual(rss_item.title, 'bar')
            self.assertEqual(rss_item.link, 'baz')
            self.assertEqual(rss_item.description, 'qux')

            db.update_publish('foo')
            with self.assertRaises(RowNotFoundError):
                db.select_first_unpublished()

            [full_rss_item] = list(db.full_rss_items())
            self.assertEqual('foo', full_rss_item.guid)
            self.assertEqual('bar', full_rss_item.title)
            self.assertEqual('baz', full_rss_item.link)
            self.assertEqual('qux', full_rss_item.description)
            self.assertIsNotNone(full_rss_item.creation_date)
            self.assertIsNotNone(full_rss_item.published_date)
