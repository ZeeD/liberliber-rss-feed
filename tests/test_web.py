from concurrent.futures.thread import ThreadPoolExecutor
from unittest import TestCase
from urllib.request import urlopen

from _support.factories import c
from liberliber_rss_feed.db import db_connection
from liberliber_rss_feed.web import serve_webui


class TestWeb(TestCase):
    maxDiff = None

    def test_serve_webui(self) -> None:
        with (
            db_connection(c(sqlfn=':memory:')) as db,
            ThreadPoolExecutor() as executor
        ):
            executor.submit(serve_webui, db)
            response = urlopen('http://localhost:8000')
            self.assertIsNotNone(serve_webui.httpd)
            if serve_webui.httpd is not None:
                serve_webui.httpd.shutdown()
        self.assertEqual(
            """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="icon" href="data:;base64,=" />
        <title>mood of the day</title>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>id</th>
                    <th>artist</th>
                    <th>title</th>
                    <th>youtube_url</th>
                    <th>creation_date</th>
                    <th>published_date</th>
                </tr>
            </thead>
            <tbody>

            </tbody>
        </table>
    </body>
</html>
""",
            response.read().decode('UTF-8'),
        )
