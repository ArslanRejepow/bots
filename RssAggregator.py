FEED_URLS = [{'url': 'https://turkmenportal.com/rss/tm', 'image' : "enclosure", 'pre': 'https://turkmenportal.com'},
{'url': 'https://www.atavatan-turkmenistan.com/feed/', 'image':'in_description', 'pre': False},
{'url': 'https://business.com.tm/rss/tm', 'image': 'enclosure', 'pre': False},
{'url': 'https://turkmensport.com/feed', 'image': 'in_description', 'pre': False},
{'url': 'https://turkmengazet.com/feed/', 'image': 'in_description', 'pre': False},
{'url': 'https://jeyhun.news/tk/feed/', 'image': 'in_description', 'pre': False},
{'url': 'https://gorogly.com/feed/', 'image': 'in_description', 'pre': False},
{'url': 'https://www.ylymly.com/feed/', 'image': False, 'pre': False},
{'url': 'https://okde.com.tm/tm/feed/', 'image': False, 'pre': False},
{'url': 'https://zamanturkmenistan.com.tm/?feed=rss2', 'image': False, 'pre': False},
{'url': 'https://www.tdob.gov.tm/feed/', 'image': False, 'pre': False},
{'url': 'https://www.trt.net.tr/turkmen/all.rss', 'image': False, 'pre': False},
{'url': 'https://orient.tm/tm/rss', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/syyasat_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/ykdysadyyet_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/jemgyyet_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/ylym_bilim_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/tehnologiya_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/saglyk_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://salamnews.tm/sport_tm.xml', 'image': 'enclosure', 'pre': False},
{'url': 'https://silkroadtm.jp/tm/rss', 'image': 'enclosure', 'pre': False}]

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
