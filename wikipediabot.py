import requests, wikipedia, random, pymysql
from bs4 import BeautifulSoup as bs

class WikipediaBot:
  def __init__(self, link, lang):
    langs = {'tk': 'Ýörite:AllPages', 'ru': 'Служебная:Все страницы'}
    self.link = link
    self.lang_tag = langs[lang]
    self.control = 2
    self.prelink = 'https://'+lang+'.wikipedia.org'
    self.lang = lang

    wikipedia.set_lang(lang)

  def get_url(self):
    print(self.link)
    r = requests.get(self.link)
    self.soup = bs(r.content, 'html.parser')
  
  def get_summary(self, title):
    summary = wikipedia.page(title)
    return summary

  def get_all_titles(self):
    titles = self.soup.find('ul', attrs = {'class': 'mw-allpages-chunk'}).find_all('li')
    for i in titles:
      yield self.prelink + i.find('a')['href'], i.find('a').text

  def get_next_page(self):
    next = self.soup.find_all('a', attrs= {'title': self.lang_tag})
    print(next)
    if len(next) == self.control:
      self.control = 4
      self.link = self.prelink+next[1]['href']

  def get_image(self, title):
    url = 'https://'+self.lang+'.wikipedia.org/w/api.php?action=query&titles='+title+'&prop=pageimages&format=json&pithumbsize=200'
    r = requests.get(url).json()
    page_id = next(iter(r['query']['pages']))
    try:
      return r['query']['pages'][page_id]['thumbnail']['source']
    except:
      return None

  def download_image(self, url):
    print(url)
    img_data = requests.get(url).content
    rand_num = random.randint(1000000,100000000)
    filename = url.split('/')[-1:][0]
    with open(str(rand_num)+filename, 'wb') as handler:
        handler.write(img_data)
    return str(rand_num)+filename
  def save_to_db(self, title, summary, image_path):
    db = pymysql.connect(host = '95.85.97.67', user='gozle', password='H@mraeV987123654', database='gozle_tm')
    cursor = db.cursor()
    sql = f"INSERT INTO `in_wiki` (`title`, `summary`, `image` ) VALUES ({title}, {summary}, {image_path})"
    cursor.execute(sql)

  def start(self):
    while True:
      try:
        self.get_url()
        for i, n in self.get_all_titles():
          summ = self.get_summary(n)
          summary = summ.summary
          title = summ.title
          image_url = self.get_image(title)
          image_path = ''
          if image_url:
            image_path = self.download_image(image_url)
          print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
          print(title, summary, image_path, sep='\n')
        self.get_next_page()
      except Exception as e:
        print(e)

wiki = WikipediaBot('https://tk.wikipedia.org/wiki/%C3%9D%C3%B6rite:AllPages', 'tk')
# wiki = WikipediaBot('https://tk.wikipedia.org/w/index.php?title=%C3%9D%C3%B6rite:AllPages&from=Absol%C3%BDut+geometri%C3%BDa', 'tk')
wiki.start()