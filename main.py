#!/usr/bin/env python3
# -'''- coding: utf-8 -'''-

# Qt stuff shouldn't be imported to main.py !

import urllib.parse
import time
import logging
logging.basicConfig(level=logging.DEBUG)

class Item(object):
    __slots__ = ('card', 'shop_link', 'card_amount',
        'search_link', 'html',
        'item_name',#店铺里的名字
        'item_price',
        'item_link'
        )
    def __init__(self):
        self.card = self.shop_link = self.search_link = self.html = None
        self.item_name = self.item_price = self.item_link = None
        self.card_amount = 1
    def __str__(self):
        ret = self.card + " from " + self.shop_link
        if self.item_price:
            ret = ret + " :: " + str(self.item_price)
        return ret

import os
from pathlib import Path
HOME_PATH = Path(os.path.expanduser('~'))
VAR_PATH = HOME_PATH.joinpath(".mtg_buyer")
TEMP_FOLDER = VAR_PATH.joinpath("temp")
TEMP_HTML_PAGE = TEMP_FOLDER.joinpath("index.html")
CARD_NAMES = []
SHOP_LINKS = []
ITEMS = []

def create_var_path():
    logging.warn("var_path hack for li's PC")
    Path(VAR_PATH).mkdir(parents=True, exist_ok=True)
    Path(TEMP_FOLDER).mkdir(parents=True, exist_ok=True)
create_var_path()

def calc_shop_total_price(shop_link, items):
    items = [i for i in items if i.shop_link == shop_link]
    return sum([i.item_price for i in items])

def _get_url(item:Item)->str:
    url_component = [
        item.shop_link,
        "/search.htm?q=",
        urllib.parse.quote_plus(item.card.encode('gbk')),
        "&searcy_type=item",
        "&s_from=newHeader&source=&ssid=s5-e&search=y",
        "&viewType=list",
        "&initiative_id=shopz_",
        time.strftime("%Y%m%d"),
    ]
    return "".join(url_component)

def generate_page(l:tuple)->str:
    assert(type(l[0]) == Item)
    from yattag import Doc
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('meta', charset='utf-8'):
                pass
        with tag('body'):
            with tag('div'):
                for sn in range(len(SHOP_LINKS)):
                    with tag('div', style="float:left; width:400px; border-style:solid"):
                        text(str(sn))
                        text(SHOP_LINKS[sn])
                        todo = tuple(i for i in l if i.shop_link == SHOP_LINKS[sn])
                        with tag('ul'):
                            for i in todo:
                                with tag('li'):
                                    with tag('a', href=i.item_link):
                                        text(i.item_name)
                                    text("  " + str(i.item_price))
                        with tag('div'):
                            text("Total: " + str( calc_shop_total_price(SHOP_LINKS[sn], items=todo)  ))

    return doc.getvalue()

import resolve
import selenium_browser
def search(shop_link, card_name, card_amount=1):
    i = Item()
    i.card = card_name
    i.shop_link = shop_link
    i.search_link = _get_url(i)
    i.html = selenium_browser.fetch(i.search_link)
# 同一个商店，同一张卡，可能有多个商品。这里只保留标价最低的
    return resolve.best_choice(i)


class Card(object):
    name = ""
    number = ""
    def __str__(self):
        return self.name + " : " + str(self.number)

def submit_data(shops:list, cards:list)->str:
    '''shops: list of str
    cards: list of Card()

    Return a link, pointing to result (local)
    '''
    logging.info("Submitted shops:")
    logging.info(shops)
    logging.info("Submitted cards:")
    logging.info( ", ".join(
        [i.name + ":" + str(i.number) for i in cards]))

    TEMP_HTML_PAGE = TEMP_FOLDER.joinpath("index.html")
    global SHOP_LINKS
    global CARD_NAMES
    SHOP_LINKS = list(shops)
    CARD_NAMES = [i.name for i in cards]
    print(cards)
    print(CARD_NAMES)
    for s in SHOP_LINKS:
        for c in CARD_NAMES:
            i = search(s, c)
            if i and i.item_link:
                ITEMS.append(i)
            time.sleep(0.05)
    selenium_browser.clean_up_before_quit()

    result = ITEMS
    html = generate_page(result)
    with open(TEMP_HTML_PAGE, "w") as fout:
        fout.write(html)
    return TEMP_HTML_PAGE

def run_sample():
    global ITEMS
    global TEMP_HTML_PAGE

    cards = []
    global SHOP_LINKS
    global CARD_NAMES
    print(CARD_NAMES)
    for i in CARD_NAMES:
        c = Card()
        c.name = i
        c.number = 1
        cards.append(c)

    submit_data(SHOP_LINKS, cards)

if __name__ == '__main__':
    CARD_NAMES = ["赞迪卡伙伴基定", "放出怪灵"]
    SHOP_LINKS = ["https://shop101650459.taobao.com"]
    run_sample()
