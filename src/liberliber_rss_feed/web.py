from html import escape
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from typing import TYPE_CHECKING
from typing import ClassVar
from webbrowser import open

if TYPE_CHECKING:
    from io import BufferedIOBase

    from liberliber_rss_feed.db import FullRssItem

    from .db import Db

HTML = """<!DOCTYPE html>
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
%s
            </tbody>
        </table>
    </body>
</html>
"""


def html(row: 'FullRssItem') -> str:
    return f"""<tr>
        <td>{escape(row.guid)}</td>
        <td>{escape(row.title)}</td>
        <td><a href="{escape(row.link)}">{escape(row.link)}</a></td>
        <td>{escape(row.description)}</td>
        <td>{row.creation_date}</td>
        <td>{row.published_date}</td>
    </tr>"""


def request_handler(db: 'Db') -> type[BaseHTTPRequestHandler]:
    def read(rfile: 'BufferedIOBase', size: int = 1024) -> str:
        chunks: bytes = b''
        while True:
            chunk = rfile.read1(size)
            chunks += chunk
            if len(chunk) < size:
                break
        return chunks.decode()

    class RequestHandler(BaseHTTPRequestHandler):
        db: ClassVar['Db']

        def do_GET(self) -> None:  # noqa: N802
            self.log_message('GET')
            self.log_request(200)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                HTML.replace(
                    '%s', '\n'.join(map(html, self.db.full_rss_items()))
                ).encode()
            )
            self.wfile.flush()

    RequestHandler.db = db
    return RequestHandler


class ServeWebui:
    httpd: ThreadingHTTPServer | None = None

    def __call__(self, db: 'Db', *, open_browser: bool = False) -> None:
        if self.httpd is not None:
            raise ValueError
        self.httpd = ThreadingHTTPServer(('', 8000), request_handler(db))
        if open_browser:
            open('localhost:8000')
        self.httpd.serve_forever()


serve_webui = ServeWebui()
