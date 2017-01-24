from main import Item, TEMP_FOLDER
import logging
from bs4 import BeautifulSoup
import copy

def _deeper(i, sons=1, pos=None):
    '''只是向下挖一层'''
    c = [k for k in i.contents  if str(k).strip()]
    assert(len(c) == sons)
    if(sons == 1):
        return c[0]
    else:
        return c[pos]

def _dewrap(li):
    li = _deeper(li) #<dl class="item">
    li = _deeper(li, 2, 1) #<dd class="detail-info">
    return li

def _extract(item:Item, e):
    '''e: bs4.element.Tag'''
    item = copy.copy(item)
    c = [k for k in e.contents  if str(k).strip()]

    title = c[0]
    text = title.text.strip()
    item.item_name = text

    price = c[1]
    after_discount = [k for k in price.contents  if str(k).strip()][0]
    p = None
    for i in after_discount:
        if 'value' in i.attrs['class']:
            p = float(i.text)
    assert(p)
    item.item_price = p

    return item

def resolve(item:Item):
    logging.warn("resolve " + item.card)
    soup = BeautifulSoup(item.html, 'html.parser')
    elements = soup.find_all('li', class_='item-wrap')
    elements = tuple(_dewrap(e) for e in elements)
    choices = [_extract(item, e) for e in elements]
    for c in choices:
        print(c.item_name, c.item_price)

if __name__ == '__main__':
    i = Item()
    i.html = "beef"
    i.card = "文胸"
    with open("/Users/lizhenbo/Downloads/mtg/文胸") as fin:
        i.html = fin.read()
    resolve(i)
