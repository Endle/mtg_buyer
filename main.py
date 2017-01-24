CARD_NAMES = ["背心", "文胸", "打底"]
SHOP_LINKS = ["https://shop62237807.taobao.com", "https://shop65188790.taobao.com"]

TEMP_FOLDER = "/Users/lizhenbo/Downloads/"
TEMP_HTML_PAGE = TEMP_FOLDER + "index.html"

import browser

html = browser.fetch(SHOP_LINKS[0])

with open(TEMP_HTML_PAGE, "w") as fout:
    fout.write(html)

browser.clean_up_before_quit()
