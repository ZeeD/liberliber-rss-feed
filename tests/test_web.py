from concurrent.futures.thread import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from typing import cast
from unittest import TestCase
from urllib.request import urlopen

from _support.factories import c
from liberliber_rss_feed.db import db_connection
from liberliber_rss_feed.web import serve_webui


class TestWeb(TestCase):
    def test_serve_webui(self) -> None:
        with ThreadPoolExecutor() as executor:
            with db_connection(c(sqlfn=':memory:')) as db:
                executor.submit(serve_webui, db)
                response = urlopen('http://localhost:8000')
            cast(ThreadingHTTPServer, serve_webui.httpd).shutdown()
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
                    <th>guid</th>
                    <th>title</th>
                    <th>link</th>
                    <th>description</th>
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
