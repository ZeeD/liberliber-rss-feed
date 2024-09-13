from logging import info
from typing import TYPE_CHECKING

from .cron import Cron
from .db import Db
from .db import RowNotFoundError
from .mastoclient import publish

if TYPE_CHECKING:
    from .config import Config


def _cron_push_mastodon_step(db: Db, config: 'Config') -> None:
    try:
        rss_item = db.select_first_unpublished()
    except RowNotFoundError:
        info('nothing to publish')
        return

    msg = f'{rss_item.title} ({rss_item.link})\n\n{rss_item.description}'
    publish(config, msg)
    info('published %s', msg)
    db.update_publish(rss_item.guid)


def cron_push_mastodon(db: Db, config: 'Config') -> None:
    replace_kwargs = {'hour': 20, 'minute': 0, 'second': 0, 'microsecond': 0}
    timedelta_kwargs = {'days': 1}
    cron = Cron(_cron_push_mastodon_step, (db, config))
    cron.run_forever(
        replace_kwargs=replace_kwargs, timedelta_kwargs=timedelta_kwargs
    )
