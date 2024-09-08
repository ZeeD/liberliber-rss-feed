from datetime import datetime

from liberliber_rss_feed.config import Config
from liberliber_rss_feed.dt import TZ


def dt(day: int) -> datetime:
    return datetime(2024, 1, day, tzinfo=TZ)


def c(  # noqa: PLR0913
    *,
    client_id: str = '',
    client_secret: str = '',
    access_token: str = '',
    api_base_url: str = '',
    sqlfn: str = '',
    rss_feed_url: str = '',
) -> Config:
    return Config(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=api_base_url,
        sqlfn=sqlfn,
        rss_feed_url=rss_feed_url,
    )
