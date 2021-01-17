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
            self.feedItems = []
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
            self.feedURL = BASE_URL + '/feeds/videos.xml?channel_id=' + self.uid

            # Construct cannonical channel URL (if required)
            if BASE_URL + '/c/' in self.url:
                self.url = BASE_URL + '/channel/' + self.uid
        
        raise ValueError('Invalid channel URL. Channel does not exist.\nURL: ' + self.url) 
    
    def update(self):
        """
        Request RSS and stores last feed update.
        """

        def pans(namespace:str, s:str) -> str:
            """Pre Append NameSpace. Helper to pre append a namespace to an string"""
            if namespace == 'atom':
                return '{http://www.w3.org/2005/Atom}' + s
            elif namespace == 'yt':
                return '{http://www.youtube.com/xml/schemas/2015}' + s
            elif namespace == 'media':
                return '{http://search.yahoo.com/mrss/}' + s
            else:
                raise ValueError("Invalid namespace: " + namespace)

        today = datetime.now()

        response = requests.get(self.feedURL)
        content = response.content.decode('utf-8')
        root = ET.fromstring(content)
        
        self.xml = root # Just for Debug
        
        # Find all videos in this channels' feed
        entries = root.findall(pans('atom', 'entry'))
        for entry in entries:
            self.feedItems.append({
                # Get video UID
                "uid": entry.find(pans('atom', 'id')).text.replace('yt:video:', ''),
                # Get video URL
                "url": entry.find(pans('atom', 'link')).get('href'),
                # Get video title
                "title": entry.find(pans('atom', 'title')).text,
                # Get video description
                "description": entry.find(pans('media', 'group')).find(pans('media', 'description')).text,
                # Get video thumbnail URL
                "thumbnail": entry.find(pans('media', 'group')).find(pans('media', 'thumbnail')).get('url'),
                # Get video published date
                "published": datetime.strptime(
                    entry.find(pans('atom', 'published')).text,
                    '%Y-%m-%dT%H:%M:%S%z'
                ),
                # Add video last time checked date
                "last_check": today
            })
