from logging import INFO
from logging import basicConfig

from .config import get_config
from .daemon import start_daemon
from .db import db_connection


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    config = get_config()

    with db_connection(config) as db:
        start_daemon(db, config)
