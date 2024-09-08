from pathlib import Path
from unittest import TestCase

from liberliber_rss_feed.config import get_config


class TestConfig(TestCase):
    dotenv_path = Path(__file__).with_name('test-liberliber-rss-feed.env')

    def test_get_config(self) -> None:
        config = get_config(self.dotenv_path)
        self.assertEqual('client-id', config['client_id'])
        self.assertEqual('client-secret', config['client_secret'])
        self.assertEqual('access-token', config['access_token'])
        self.assertEqual(
            'http://api-base-url.example.com', config['api_base_url']
        )
        self.assertEqual('file:sqlfn?mode=memory', config['sqlfn'])
