CARD_NAMES = ["背心", "文胸", "打底"]
SHOP_LINKS = ["https://shop62237807.taobao.com", "https://shop65188790.taobao.com"]

TEMP_FOLDER = "/Users/lizhenbo/Downloads/"
TEMP_HTML_PAGE = TEMP_FOLDER + "index.html"

class Item(object):
    __slots__ = 'card', 'shop_link', 'search_link', 'html'

import selenium_browser

for c in CARD_NAMES:
    for s in SHOP_LINKS:
        i = Item()
        i.card = c
        i.shop_link = s
        i.search_link = SHOP_LINKS[0]
        i.html = selenium_browser.fetch(i.search_link)

html = selenium_browser.fetch(SHOP_LINKS[0])

with open(TEMP_HTML_PAGE, "w") as fout:
    fout.write(html)

selenium_browser.clean_up_before_quit()
