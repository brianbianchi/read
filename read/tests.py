import unittest
from django.test import TestCase
from .views import get_rss_feed

class TestGetRssFeed(TestCase):
    def test_missing_url(self):
        self.assertIsNone(get_rss_feed(None))

    def test_invalid_url(self):
        self.assertIsNone(get_rss_feed('http://example.com'))
        self.assertIsNone(get_rss_feed('ftp://example.com'))

    def test_reddit_url(self):
        reddit_url = 'https://www.reddit.com/r/Python/'
        self.assertEqual(get_rss_feed(reddit_url), str(reddit_url + 
'.rss'))

    def test_reddit_url_no_slash(self):
        reddit_url = 'https://www.reddit.com/r/Python'
        self.assertEqual(get_rss_feed(reddit_url), str(reddit_url + 
'/.rss'))

if __name__ == '__main__':
    unittest.main()
