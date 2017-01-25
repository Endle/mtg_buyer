class Item(object):
    __slots__ = ('card', 'shop_link', 'search_link', 'html',
        'item_name',#店铺里的名字
        'item_price',
        'item_link'
        )

TEMP_FOLDER = "/Users/lizhenbo/Downloads/mtg/"
CARD_NAMES = []
SHOP_LINKS = []

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

    return doc.getvalue()

def main():
    import selenium_browser

    TEMP_HTML_PAGE = TEMP_FOLDER + "index.html"

    ITEMS = []

    for s in SHOP_LINKS[:1]:
        for c in CARD_NAMES[:1]:
            i = Item()
            i.card = c
            i.shop_link = s
            i.search_link = _get_url(i)
            i.html = selenium_browser.fetch(i.search_link)
            ITEMS.append(i)
            time.sleep(0.05)

    selenium_browser.clean_up_before_quit()

    import resolve
    result = tuple(resolve.resolve(i) for i in ITEMS)
# 同一个商店，同一张卡，可能有多个商品。这里只保留标价最低的
    result = tuple(i[0] for i in result)
    html = generate_page(result)
    with open(TEMP_HTML_PAGE, "w") as fout:
        fout.write(html)


if __name__ == '__main__':
    CARD_NAMES = ["背心", "文胸", "打底"]
    SHOP_LINKS = ["https://shop62237807.taobao.com", "https://shop65188790.taobao.com"]
    main()
