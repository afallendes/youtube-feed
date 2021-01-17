import re
from xml.etree import ElementTree as ET

import requests

class YouTubeChannel:
    def __init__(self, url):
        BASE_URL = 'https://www.youtube.com'
        
        if any([
            url.startswith(BASE_URL + '/c/'),
            url.startswith(BASE_URL + '/channel/')
        ]):
            self.url = url
        else:
            raise ValueError('Invalid channel URL: ' + url)
    
    def get(self):
        """
        Requests and saves basic information of the channel.
        """
        response = requests.get(self.url)
        content = response.content.decode('utf-8')

        # Get RSS
        re_pattern = r'\"rssUrl\":\"(?P<rss>https:\/\/www.youtube\.com/feeds\/videos\.xml\?channel_id\=\w*)",'
        re_search = re.search(re_pattern, content)
        self.rss = re_search.group('rss')
        
        # Get UID and Title
        re_pattern = r'\"channelId\":\"(?P<uid>\w*)",\"title\":\"(?P<title>.*)\",\"navigationEndpoint\"'
        re_search = re.search(re_pattern, content)
        self.uid = re_search.group('uid')
        self.title = re_search.group('title')

        # Get Avatar
        re_pattern = r'\"avatar\":\{\"thumbnails\":\[\{\"url\":\"(?P<avatar>https:\/\/yt3.ggpht.com\/ytc\/[\w_-]*)=s'
        re_search = re.search(re_pattern, content)
        self.avatar = re_search.group('avatar')

