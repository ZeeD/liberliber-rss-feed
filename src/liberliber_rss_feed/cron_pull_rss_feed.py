from typing import TYPE_CHECKING

from .cron import Cron
from .rssclient import fetch

if TYPE_CHECKING:
    from .config import Config
    from .db import Db


def _cron_pull_rss_feed_step(db: 'Db', config: 'Config') -> None:
    for row in fetch(config):
        db.upsert(row)


def cron_pull_rss_feed(db: 'Db', config: 'Config') -> None:
    replace_kwargs = {'hour': 8, 'minute': 0, 'second': 0, 'microsecond': 0}
    timedelta_kwargs = {'days': 1}
    cron = Cron(_cron_pull_rss_feed_step, (db, config))
    cron.run_forever(
        replace_kwargs=replace_kwargs, timedelta_kwargs=timedelta_kwargs
    )
