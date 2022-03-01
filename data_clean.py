import os
from bs4 import BeautifulSoup
import pandas as pd
import re
import string
import nltk
'''
    For the given path, get the List of all files in the directory tree 
'''

class janitor():
    def __init__(self, dirName):
          self.dirName = dirName

    def get_files_paths(self):
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(dirName):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        return listOfFiles

    def clean(listOfFiles):
        article_list = []
        #for file in listOfFiles[:5]:
        for file in listOfFiles:
            if not file.endswith('DS_Store'):
                content = open(file, 'r')
                soup = BeautifulSoup(content, features='xml')
                articles = soup.findAll('item')      
                for a in articles:
                    #print(a)
                    if a.find('content:encoded'):
                        title = a.find('title').text
                        print(title)
                        link = a.find('link').text
                        published = a.find('pubDate').text
                        description = a.find('content:encoded').text
                        re_xml = re.compile(r'<[^>]+>')
                        remove_tags = re_xml.sub('', description)
                        re_code = re.compile(r'&#\d\d\d\d;')
                        remove_codes = re_code.sub('', remove_tags)
                        lower = remove_codes.lower()
                        encoded = lower.encode('ascii', 'ignore')
                        decoded = encoded.decode()
                        rmv_punc = re.sub('[%s]' % re.escape(string.punctuation), '', lower)
                        rmv_2 = re.sub('[‘’“”…]', '', rmv_punc)
                        rmv_3 = re.sub('\n', '', rmv_2)
                        #print(rmv_3)
                        #print(description)
                        article = {
                            'title': title,
                            'link': link,
                            'published': published,
                            'content': rmv_3
                            }
                        article_list.append(article)
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame.from_dict(article_list)
        df.to_csv('gather.csv')
        return df


   
if __name__ == '__main__':
    dirName = '/Users/tanguyen/Documents/ML/scraper/feeds/krebs';
    fullPathFileList = janitor.get_files_paths(dirName)
    gather = janitor.clean(fullPathFileList)
    #cleaned = janitor.clean(gather)
    #print(cleaned)
    #with open('gather.csv', 'w') as f:
    #    f.write(str(gather))




        