import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import csv

def get_soup(URL, CHROMEDRIVER_PATH):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(CHROMEDRIVER_PATH,options=options)
    driver.get(URL)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    driver.close()
    return soup.find_all(name = 'div', class_ ='lister-item mode-advanced')

def get_data(el):
    director_stars = el.find_all(name ='p')[2].get_text().replace('\n', '').strip()
    data = {}

    try:
        data['name'] = el.find(name ='h3', class_ = 'lister-item-header').find(name='a').get_text().replace('\n', '').strip(),
    except:
        data['name'] = None

    try:
        data['year'] = el.find(name ='h3', class_ = 'lister-item-header').find(name='span', class_ = 'lister-item-year text-muted unbold').get_text()[1:-1].replace('\n', '').strip(),
    except:
        data['year'] = None

    try:
        data['certificate'] = el.find(name ='span', class_ = 'certificate').get_text().replace('\n', '').strip(),
    except:
        data['certificate'] = None

    try:
        data['runtime'] = el.find(name ='span', class_ = 'runtime').get_text().replace('\n', '').strip(),
    except:
        data['runtime'] = None

    try:
        data['genre'] = el.find(name ='span', class_ = 'genre').get_text().replace('\n', '').strip().split(', '),
    except:
        data['genre'] = None

    try:
        data['rating'] = el.find(name ='div', class_ = 'inline-block ratings-imdb-rating').find(name='strong').get_text().replace('\n', '').strip(),
    except:
        data['rating'] = None

    try:
        data['desc'] = el.find_all(name ='p', class_ = 'text-muted')[1].get_text().replace('\n', '').strip(),
    except:
        data['desc'] = None

    try:
        data['director'] =  re.findall(r'Director:(.*)\|', director_stars)[0],
    except:
        data['director'] = None

    try:
        data['stars'] =  re.findall(r'Stars:(.*)', director_stars)[0].split(', '),
    except:
        data['stars'] = None

    try:
        data['votes'] =  el.find(name ='p', class_ = 'sort-num_votes-visible').find_all(name='span')[1].get_text().replace('\n', '').strip()
    except:
        data['votes'] = None

    
    return data


if __name__ == '__main__':
    CHROMEDRIVER_PATH = '/home/skerr1q/Downloads/chromedriver'
    URL = 'https://www.imdb.com/search/title/?title_type=short&sort=num_votes,desc&start=1&ref_=adv_nxt'
    soup = get_soup(URL, CHROMEDRIVER_PATH)
    records = []
    for i in range(50):
        data = get_data(soup[i])
        records.append(data)
    
    with open('records.csv','w') as f:
        w = csv.DictWriter(f,records[0].keys())
        w.writerows(records)