from main import Item, TEMP_FOLDER
import logging
from bs4 import BeautifulSoup

def _dewrap(li):
    def _deeper(i, sons=1, pos=None):
        '''只是向下挖一层'''
        c = [k for k in i.contents  if str(k).strip() ]
        assert(len(c) == sons)
        if(sons == 1):
            return c[0]
        else:
            return c[pos]
    li = _deeper(li) #<dl class="item">
    li = _deeper(li, 2, 1) #<dd class="detail-info">
    print("===")
    print(li)
    return li

def resolve(item:Item):
    logging.warn("resolve " + item.card)
    soup = BeautifulSoup(item.html, 'html.parser')
    elements = soup.find_all('li', class_='item-wrap')
    elements = tuple(_dewrap(e) for e in elements)

if __name__ == '__main__':
    i = Item()
    i.html = "beef"
    i.card = "文胸"
    with open("/Users/lizhenbo/Downloads/mtg/文胸") as fin:
        i.html = fin.read()
    resolve(i)
