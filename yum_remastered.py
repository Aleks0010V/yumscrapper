import csv, time
from bs4 import BeautifulSoup
from requests import get

h = {'Host': 'yummyanime.club',
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
'Accept': 'text/css,*/*;q=0.1',
'Accept-Language': 'en,en-US;q=0.5'}

class Title():
    global h
    def get_info(link):
        genres = list()
        html = get(link, headers=h)
        print(html.status_code)
        try:
            html = BeautifulSoup(html.text, 'html.parser')
            title = html.select('h1')[0].text.strip()
            html = html.find_all('ul', class_="categories-list")[0]
            for tag in html.select('a'):
                genres.append(tag.text)
        except:
            title, genres = [f'{html.status_code}'] * 2
        return (title, genres)

    def __init__(self, link):
        self.link = link
        self.title, self.genres = Title.get_info(link)
        try:
            self.genres.sort()
        except:
            pass

    def __str__(self):
        return f'{self.link}, {self.title}, {self.genres}'

def get_links():
    global name, h
    links = list()
    url = input('Enter a link to profile: ')
    id = url.split('/')[4]
    html = get(url, headers=h)
    html = BeautifulSoup(html.text, 'html.parser')
    with open('page1.html', 'w') as handle:
        handle.write((str(html('div', id="watched")[0])))
    with open('page1.html', 'r') as handle:
        html = handle.read()
        html = BeautifulSoup(html, 'html.parser')
        for el in html.select('a'):
            links.append(f"https://yummyanime.club{el['href']}")
    return (links, id)

def get_titles(links):
    titles = list()
    for link in links:
        a = Title(link)
        titles.append((a.link, a.title, a.genres))
        time.sleep(0.65)
    return titles

links, id = get_links()
titles = get_titles(links)
with open(f'{id}.csv', 'w') as handle:
    handle.write('link;title;genres\n')
    for title in titles:
        handle.write(f"{title[0]};{title[1]};{' '.join(title[2])}\n")
