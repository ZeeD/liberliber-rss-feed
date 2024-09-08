from typing import TYPE_CHECKING
from urllib.request import urlopen

from defusedxml.ElementTree import fromstring

from .db import RssItem

if TYPE_CHECKING:
    from .config import Config


def fetch(config: 'Config') -> list[RssItem]:
    channel = fromstring(urlopen(config['rss_feed_url']).read())[0]  # noqa: S310
    rows = []
    for item in channel.findall('item'):
        guid = item.find('guid')
        if guid is None or guid.text is None:
            raise ValueError
        title = item.find('title')
        if title is None or title.text is None:
            raise ValueError
        link = item.find('link')
        if link is None or link.text is None:
            raise ValueError
        description = item.find('description')
        if description is None or description.text is None:
            raise ValueError
        rows.append(RssItem(guid.text, title.text, link.text, description.text))
    return rows
