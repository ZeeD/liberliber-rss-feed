from logging import INFO
from logging import basicConfig

from liberliber_rss_feed.config import get_config
from liberliber_rss_feed.daemon import start_daemon
from liberliber_rss_feed.db import db_connection


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    config = get_config()

    with db_connection(config) as db:
        start_daemon(db, config)
