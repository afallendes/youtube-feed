import re
from xml.etree import ElementTree as ET
from datetime import datetime

import requests

BASE_URL = 'https://www.youtube.com'

class YouTubeChannel:
    def __init__(self, url):
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

        if response.status_code == '200':
            content = response.content.decode('utf-8')

            # Get UID and Title
            re_pattern = r'\"channelId\":\"(?P<uid>\w*)",\"title\":\"(?P<title>.*)\",\"navigationEndpoint\"'
            re_search = re.search(re_pattern, content)
            self.uid = re_search.group('uid')
            self.title = re_search.group('title')

            # Get Avatar
            re_pattern = r'\"avatar\":\{\"thumbnails\":\[\{\"url\":\"(?P<avatar>https:\/\/yt3.ggpht.com\/ytc\/[\w_-]*)=s'
            re_search = re.search(re_pattern, content)
            self.avatar = re_search.group('avatar')

            # Construct Feed URL
            self.rss = BASE_URL + '/feeds/videos.xml?channel_id=' + self.uid

            # Construct cannonical channel URL (if required)
            if BASE_URL + '/c/' in self.url:
                self.url = BASE_URL + '/channel/' + self.uid
        
        raise ValueError('Invalid channel URL. Channel does not exist.\nURL: ' + self.url) 
    
    def update(self):
        """
        Request RSS and stores last feed update.
        """

        def pre_append_namespace(s):
            """Helper to pre append a namespace to an string"""
            return '{http://www.w3.org/2005/Atom}' + s

        today = datetime.now()

        response = requests.get(self.rss)
        content = response.content.decode('utf-8')
        root = ET.fromstring(content)
        
        self.xml = root # Just for Debug
        
        # Find all videos in this channels' feed
        entries = root.findall(pre_append_namespace('entry'))
        for entry in entries:
            self.feed.append({
                # Get video UID
                "uid": entry.find(pre_append_namespace('id')).text.replace('yt:video:', ''),
                # Get video Title
                "title": entry.find(pre_append_namespace('title')).text,
                # Get video URL
                "url": entry.find(pre_append_namespace('link')).get('href'),
                # Get video published date
                "published": datetime.strptime(
                    entry.find(pre_append_namespace('published')).text,
                    '%Y-%m-%dT%H:%M:%S%z'
                ),
                # Add video last time checked date
                "last_check": today
            })
