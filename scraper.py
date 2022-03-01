import requests
from bs4 import BeautifulSoup

class scraping():
    def __init__(self, rsslink):
        self.rsslink = rsslink

    def hackernews_rss(self):
        article_list = []
        r = requests.get(rsslink)
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')        
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            article = {
                'title': title,
                'link': link,
                'published': published
                }
            article_list.append(article)
        return article_list

if __name__ == "__main__":
    print('Starting scraping')
    rsslink='https://krebsonsecurity.com/feed/'
    scraping = scraping.hackernews_rss(rsslink)
    print(scraping)
