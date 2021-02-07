# YouTube Channel Information Scrapper

import re
from xml.etree import ElementTree as ET
from datetime import datetime

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import requests



class YouTubeChannelScraper:
    YOUTUBE_BASE_URL = 'https://www.youtube.com'
    
    def __init__(self, url):
        self.url = self._validate_channel_url(url)
        
    def _validate_channel_url(self, channel_url):
        """
        Validates if 'channel_url' is a proper YouTube channel URL string. If 'channel_url' passes
        the required checks then it is returned else an error is raised.
        """
        if not isinstance(channel_url, str):
            raise TypeError('URL was not an string.')
        if len(channel_url) == 0:
            raise ValueError("URL was an empty string.")
        if not any([channel_url.startswith(_) and len(channel_url) > len(_) for _ in (
            YOUTUBE_BASE_URL + '/c/',
            YOUTUBE_BASE_URL + '/channel/',
            YOUTUBE_BASE_URL + '/user/'
        )]):
            raise ValueError("URL was not a proper YouTube channel URL.")
        return channel_url
    
    def _validate_rss_url(self, rss_url):
        RSS_BASE_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id='
        if rss_url.startswith(RSS_BASE_URL) and len(rss_url) > len(RSS_BASE_URL):
            return rss_url
        raise ValueError("RSS URL was not a proper YouTube channel URL.")

    def __validate_url(self, url, url_type):
        # Validate generic URL
        url_validator = URLValidator()
        try:
            url_validator(url)
        except ValidationError:
            raise ValidationError("URL was not valid.")
        
        # Validate YouTube channel URL
        if url_type == 'channel':
            for _ in (
                YOUTUBE_BASE_URL + '/c/',
                YOUTUBE_BASE_URL + '/channel/',
                YOUTUBE_BASE_URL + '/user/'
            ):


            if any(
                [channel_url.startswith(_) and len(channel_url.replace(_, '', 1)) > 0 for _ in (
                YOUTUBE_BASE_URL + '/c/',
                YOUTUBE_BASE_URL + '/channel/',
                YOUTUBE_BASE_URL + '/user/'
            )]):
                raise ValidationError("URL was not a proper YouTube channel URL.")
        
        # Validate YouTube channel RSS URL
        if url_type == 'rss':
            RSS_BASE_URL = YOUTUBE_BASE_URL + '/feeds/videos.xml?channel_id='
            if (
                rss_url.startswith(RSS_BASE_URL)
                and len(url.replace(RSS_BASE_URL, '', 1))
            ):
                return url
            raise ValidationError("RSS URL was not a proper YouTube channel URL.")


    def capture(self):
        """
        Requests and capture basic information channel information.
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            content = response.content.decode('utf-8')

            # Get UID and title
            re_pattern = r'\"channelId\":\"(?P<uid>[a-zA-Z0-9-_]*)",\"title\":\"(?P<title>.*)\",\"navigationEndpoint\"'
            re_search = re.search(re_pattern, content)
            self.uid = re_search.group('uid')
            self.title = re_search.group('title')

            # Get avatar
            re_pattern = r'\"avatar\":\{\"thumbnails\":\[\{\"url\":\"(?P<avatar>https:\/\/yt3.ggpht.com\/ytc\/[\w_-]*)=s'
            re_search = re.search(re_pattern, content)
            self.avatar = re_search.group('avatar')

            # Construct RSS feed
            self.rss = YOUTUBE_BASE_URL + '/feeds/videos.xml?channel_id=' + self.uid

            # Construct cannonical channel URL (if required)
            if not self.url.startswith(YOUTUBE_BASE_URL + '/channel/'):
                self.url = YOUTUBE_BASE_URL + '/channel/' + self.uid
        
        elif response.status_code == 404:
            raise ValueError('Channel does not exist.\nURL: ' + self.url) 
        else:
            raise ValueError('Channel could not be reached.\nURL: ' + self.url)

    def update(self, rss=None):
        """
        Request RSS and stores last feed update.
        """

        if rss is None:
            rss = self.rss
        else:
            rss = self._validate_rss_url(rss)

        def pans(namespace:str, s:str) -> str:
            """Helper to pre append a namespace to an string"""
            if namespace == 'atom':
                return '{http://www.w3.org/2005/Atom}' + s
            elif namespace == 'yt':
                return '{http://www.youtube.com/xml/schemas/2015}' + s
            elif namespace == 'media':
                return '{http://search.yahoo.com/mrss/}' + s
            else:
                raise ValueError("Invalid namespace: " + namespace)

        response = requests.get(rss)

        if response.status_code == 200:
            rss_entries = []
            
            root = ET.fromstring(response.content.decode('utf-8'))
            
            # Find all videos in this channels' feed
            entries = root.findall(pans('atom', 'entry'))
            for entry in entries:
                # Get video UID
                uid = entry.find(pans('atom', 'id')).text.replace('yt:video:', '')
                # Get video URL
                url = entry.find(pans('atom', 'link')).get('href')
                # Get video title
                title = entry.find(pans('atom', 'title')).text
                # Get video description
                description = entry.find(pans('media', 'group')).find(pans('media', 'description')).text
                # Get video thumbnail URL
                thumbnail = entry.find(pans('media', 'group')).find(pans('media', 'thumbnail')).get('url')
                thumbnail = thumbnail.replace('default', '720')
                # Get video published date
                published = datetime.strptime(
                    entry.find(pans('atom', 'published')).text,
                    '%Y-%m-%dT%H:%M:%S%z'
                )

                rss_entries.append({
                    "uid": uid,
                    "url": url,
                    "title": title,
                    "description": description,
                    "thumbnail": thumbnail,
                    "published": published,
                    # Add video last time checked date
                    "last_check": datetime.now()
                })
            
            return rss_entries

        elif response.status_code == 404:
            raise ValueError('RSS channel does not exist.\nURL: ' + self.url) 
        else:
            raise ValueError('RSS channel could not be reached.\nURL: ' + self.url)

url = 'https://www.youtube.com/user/j0mth'
channel = YouTubeChannelScraper(url)
channel.update('https://www.youtube.com/feeds/videos.xml?channel_id=UC5PJJOCyKs0A5fJilPRA6BA')