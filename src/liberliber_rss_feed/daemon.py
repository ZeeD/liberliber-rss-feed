from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from .cron_pull_rss_feed import cron_pull_rss_feed
from .cron_push_mastodon import cron_push_mastodon
from .web import serve_webui

if TYPE_CHECKING:
    from .config import Config
    from .db import Db


def start_daemon(db: 'Db', config: 'Config') -> None:
    with ThreadPoolExecutor() as executor:
        executor.submit(serve_webui, db)
        executor.submit(cron_push_mastodon, db, config)
        executor.submit(cron_pull_rss_feed, db, config)
