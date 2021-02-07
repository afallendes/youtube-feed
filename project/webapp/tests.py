from django.test import TestCase

from .logic import YouTubeChannel

class LogicTests(TestCase):

    def test_init_YouTubeChannel_with_c_type_url(self):
        """
        Initialize YouTubeChannel with "c" type URL (example: https://www.youtube.com/c/TrashTaste).
        This is a valid URL and should pass.
        """
        channel_url = "https://www.youtube.com/c/TrashTaste"
        self.assertNotEqual(YouTubeChannel(channel_url), ValueError)
    
    def test_init_YouTubeChannel_with_channel_type_url(self):
        """
        Initialize YouTubeChannel with "channel" type URL (example: https://www.youtube.com/channel/UCS9uQI-jC3DE0L4IpXyvr6w).
        This is a valid URL and should pass.
        """
        channel_url = "https://www.youtube.com/channel/UCS9uQI-jC3DE0L4IpXyvr6w"
        self.assertNotEqual(YouTubeChannel(channel_url), ValueError)
    
    def test_init_YouTubeChannel_with_invalid_url(self):
        """
        Initialize YouTubeChannel with any invalid value. This should raise an ValueError.
        """
        channel_url = "https://www.youtube.com/chanel/UCS9uQI-jC3DE0L4IpXyvr6w"
        self.assertRaises(ValueError, YouTubeChannel, channel_url)
    
    def test_channel_exists(self):
        pass

