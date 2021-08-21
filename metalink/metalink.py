from bs4 import BeautifulSoup
import requests


short_watch_url= "https://youtu.be/"
long_watch_url= 'https://www.youtube.com/watch?v='

class Video:
    def __init__(self, URLorID=None):
        """
        :rtype: object
        """
        if long_watch_url in URLorID:
            self.URL = URLorID
            self.id = self.extract_video_id(self.URL)
        elif short_watch_url in URLorID:
            self.URL = URLorID
            self.id = self.extract_video_id(self.URL)
        else:
            self.id = URLorID
            self.URL = long_watch_url + URLorID
        self.soup = self.fetch_html()
        self.title = self.get_title()
        self.description = self.get_description()
        self.thumbnail_URL = self.get_thumbnail_URL()
        self.keywords = self.get_keywords()
        self.domain = "video.geniuslounge.com"
### Start Methods

    def extract_video_id(self,URL):
        x= URL.replace(short_watch_url,'').replace(long_watch_url,'')
        return x

    def fetch_html(self):
        """Takes a Video class object and fetches the HTML for it, and appends it to the object"""
        request=requests.get(self.URL)
        self.html = request.content
        return BeautifulSoup(self.html, 'html.parser')

    def get_title(self):
        """Extracts the title from the HTML, and appends it to the object"""
        return self.soup.find(property="og:title")['content']

    def get_description(self):
        """Extracts the description from the HTML, and appends it to the object"""
        return self.soup.find(property="og:description")['content']

    def get_thumbnail_URL(self):
        """Extracts the Thumbnail URL from the HTML, and appends it to the object"""
        return self.soup.find(property="og:image")['content']

    def get_keywords(self):
        """Extracts the keywords from the HTML, and appends it to the object"""
        meta = self.soup.find_all('meta')

        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['keywords']:
                return tag.attrs['content']

