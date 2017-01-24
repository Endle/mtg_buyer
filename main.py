class Item(object):
    __slots__ = 'card', 'shop_link', 'search_link', 'html'

TEMP_FOLDER = "/Users/lizhenbo/Downloads/mtg/"

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

def main():
    import selenium_browser
    CARD_NAMES = ["背心", "文胸", "打底"]
    SHOP_LINKS = ["https://shop62237807.taobao.com", "https://shop65188790.taobao.com"]

    TEMP_HTML_PAGE = TEMP_FOLDER + "index.html"

    ITEMS = []

    for s in SHOP_LINKS[:1]:
        for c in CARD_NAMES:
            i = Item()
            i.card = c
            i.shop_link = s
            i.search_link = _get_url(i)
            i.html = selenium_browser.fetch(i.search_link)
            ITEMS.append(i)
            time.sleep(0.5)

    selenium_browser.clean_up_before_quit()

    import resolve
    for i in ITEMS:
        resolve.resolve(i)

if __name__ == '__main__':
    main()
