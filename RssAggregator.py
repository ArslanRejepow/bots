FEED_URLS = [{'url': 'RSS URL', 'image' : "IMAGE", 'pre': 'LINK'}]

import feedparser
import html
from bs4 import BeautifulSoup as bs
import requests

class WhizRssAggregator():
    feedurl = ""

    def __init__(self, paramrssurl, image, pre=None):
        print(paramrssurl)
        self.feedurl = paramrssurl
        self.image = image
        self.pre = pre
        self.parse()
    def get_image_from_enclosure(self, feed):
        try:
            image = feed.get('links', '')[1]['url']
        except:
            return None
        return image
    
    def get_image_from_description(self, feed):
        try:
            description = feed.get('description', '')
            soup = bs(description, 'html.parser')
            link = soup.find("img")
            return link['src']
        except:
            return None
    def download_image(self, url, path= './'):
        img_data = requests.get(url).content
        filename = url.split('/')[-1]
        with open(path+filename, 'wb') as handler:
            handler.write(img_data)
        print('[DOWNLOADED SUCCESSFULLY]' + filename)

    def parse(self):
        thefeed = feedparser.parse(self.feedurl)

        print("Getting Feed Data")
        print(thefeed.feed.get("title", ""))
        print(thefeed.feed.get("link", ""))
        print(thefeed.feed.get("description", ""))
        print(thefeed.feed.get("published", ""))

        for thefeedentry in thefeed.entries:
            title = thefeedentry.get("title", "")
            link = thefeedentry.get("link", "")
            pubDate = thefeedentry.get("published", "")
            category = thefeedentry.get("category", "")
            guid = thefeedentry.get("guid", "")
            description = thefeedentry.get("description", "")
            content = None
            if self.image == 'enclosure':
              # print(thefeedentry)
            	image = self.get_image_from_enclosure(thefeedentry)
              # print(image)
            elif self.image == 'in_description':
            	image = self.get_image_from_description(thefeedentry)
            else:
            	image = None

            if image:
            	if self.pre:
        		    self.download_image(self.pre + image, "./uploads/")
            	else:
          		    self.download_image(image, "./uploads/")

            if thefeedentry.get("content", ""):
            	content = html.unescape(thefeedentry.get("content", "")[0]['value'])
            print("----------------------------------")
            print(f"""
            title: {title}
            link: {link}
            pubDate: {pubDate}
            category: {category}
            guid: {guid}
            description: {description}
            image: {image}
            content: {content}
            """)
            
for item in FEED_URLS:
  if item['pre']:
    rssobject=WhizRssAggregator(item['url'], item['image'], item['pre'])
  else:
    rssobject=WhizRssAggregator(item['url'], item['image'])
