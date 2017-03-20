import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from functools import reduce
import os
def getSources():
    source_url = 'https://newsapi.org/v1/sources?language=en'
    response = requests.get(source_url).json()
    sources = []
    for source in response['sources']:
        sources.append(source['id'])
    return sources

def mapping():
    d = {}
    response = requests.get('https://newsapi.org/v1/sources?language=en')
    response = response.json()
    for s in response['sources']:
        d[s['id']] = s['category']
    return d

def category(source, m):
    try:
        return m[source]
    except:
        return 'NC'

def cleanData(path):
    data = pd.read_csv(path)
    data = data.drop_duplicates('url')
    data.to_csv(path, index=False)

def getDailyNews():
    sources = getSources()
    key = 'dd4a5a58ffcf4041b9bcb34a9f5442d1'
    url = 'https://newsapi.org/v1/articles?source={0}&sortBy={1}&apiKey={2}'
    responses = []
    for i, source in tqdm(enumerate(sources)):
        try:
            u = url.format(source, 'top',key)
            response = requests.get(u)
            r = response.json()
            for article in r['articles']:
                article['source'] = source
            responses.append(r)
        except:
            u = url.format(source, 'latest', key)
            response = requests.get(u)
            r = response.json()
            for article in r['articles']:
                article['source'] = source
            responses.append(r)
      
    news = pd.DataFrame(reduce(lambda x,y: x+y ,map(lambda r: r['articles'], responses)))
    news = news.dropna()
    news = news.drop_duplicates()
    d = mapping()
    news['category'] = news['source'].map(lambda s: category(s, d))
    news['scraping_date'] = datetime.now()
    trainFile=os.path.basename("news.csv")

    try:
        aux = pd.read_csv(trainFile)
    except:
        aux = pd.DataFrame(columns=list(news.columns))
        aux.to_csv(trainFile, encoding='utf-8', index=False)

    with open(trainFile, 'a', encoding='utf-8') as f:
        news.to_csv(f, header=False, encoding='utf-8', index=False)

    cleanData(trainFile)
    print('Done')

if __name__ == '__main__':
    getDailyNews()
