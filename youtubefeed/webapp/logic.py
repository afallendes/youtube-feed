import re
from xml.etree import ElementTree as ET
from datetime import datetime

import requests

class YouTubeChannel:
    def __init__(self, url):
        BASE_URL = 'https://www.youtube.com'
        
        if any([
            url.startswith(BASE_URL + '/c/'),
            url.startswith(BASE_URL + '/channel/')
        ]):
            self.url = url
            self.feed = []
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
    
    def update(self):
        """
        Request RSS and stores last feed update.
        """

        def pre_append_namespace(s):
            """Helper to pre append a namespace to an string"""
            return '{http://www.w3.org/2005/Atom}' + s

        response = requests.get(self.rss)
        content = response.content.decode('utf-8')
        root = ET.fromstring(content)
        self.xml = root
        root.findall(pre_append_namespace('entry'))
        entries = root.findall(pre_append_namespace('entry'))

        for entry in entries:
            self.feed.append({
                "uid": entry.find(pre_append_namespace('id')).text.replace('yt:video:', ''),
                "title": entry.find(pre_append_namespace('title')).text,
                "url": entry.find(pre_append_namespace('link')).get('href'),
                "published": datetime.strptime(
                    entry.find(pre_append_namespace('published')).text,
                    '%Y-%m-%dT%H:%M:%S%z'
                )
            })
