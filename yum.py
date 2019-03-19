from requests import get
from bs4 import BeautifulSoup
import re, sqlite3, time

baseURL = 'https://yummyanime.com'
name = None
h = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}

def get_content():
    global name
    global h
    url = input('Enter a link to profile: ')
    name = url.split('/')[4]
    handle = open('page1.html', 'w')
    str = get(url, headers=h)
    handle.write(str.text)
    handle.close()
    handle1 = open('page1.html', 'r')
    handle2 = open('page2.html', 'w')
    for line in handle1:
        handle2.write(line.lstrip())
    handle1.close()
    handle2.close()

def get_list():
    html = open('page2.html', 'r')
    handle = open('page1.html', 'w')
    html = BeautifulSoup(html, 'html.parser')
    handle.write((str(html('div', id="watched")[0])))
    handle.close()

def get_info():
    global name
    a = None
    title = None
    handle = open('page1.html', 'r')
    for line in handle:
        if re.search('^<a', line):
            href = re.findall('^<a href="(.*)">', line)[0]
            a = baseURL + href
            cur.execute(f"INSERT INTO {name}(link) VALUES('{a}')")
        if re.search('^[^<]', line):
            title = line
            cur.execute(f"UPDATE {name} SET title='{title}' WHERE link='{a}'")
        connection.commit()

def get_links():
    global name
    l = list()
    links = cur.execute(f'SELECT link FROM {name}')
    for link in links:
        l.append(link[0])
    return l

def get_genra(links):
    global s
    global h
    d = dict()
    l = len(links)
    for link in links:
        print(l)
        l-=1
        time.sleep(0.5)
        r = get(link, headers=h)
        html = BeautifulSoup(r.text, 'html.parser')
        html = html.find_all('ul', class_="categories-list")[0]
        for tag in html.select('a'):
            d[tag.text] = d.get(tag.text, 0) + 1
    l = list()
    for key, value in d.items():
        l.append((value, key))
    l.sort(reverse=True)
    for key, value in l:
        print(f"{value}: {key}")
    return l

get_content()
connection = sqlite3.connect('animeDB.sqlite')
cur = connection.cursor()
cur.execute(f"DROP TABLE IF EXISTS {name}")
cur.execute(f"CREATE TABLE IF NOT EXISTS {name}(link TEXT, title TEXT)")
connection.commit()
get_list()
get_info()
links = get_links()
get_genra(links)
connection.close()
