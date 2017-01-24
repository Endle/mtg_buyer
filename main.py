class Item(object):
    __slots__ = 'card', 'shop_link', 'search_link', 'html'

import urllib.parse
import time
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

CARD_NAMES = ["背心", "文胸", "打底"]
SHOP_LINKS = ["https://shop62237807.taobao.com", "https://shop65188790.taobao.com"]

TEMP_FOLDER = "/Users/lizhenbo/Downloads/"
TEMP_HTML_PAGE = TEMP_FOLDER + "index.html"

import selenium_browser

for c in CARD_NAMES:
    for s in SHOP_LINKS:
        i = Item()
        i.card = c
        i.shop_link = s
        i.search_link = _get_url(i)
        i.html = selenium_browser.fetch(i.search_link)

html = selenium_browser.fetch(SHOP_LINKS[0])

with open(TEMP_HTML_PAGE, "w") as fout:
    fout.write(html)

selenium_browser.clean_up_before_quit()
