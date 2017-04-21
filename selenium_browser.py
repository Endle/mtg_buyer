from selenium import webdriver
import threading
import cachetools
import logging
from pathlib import Path
import os
logger = logging.getLogger(__name__)

_driver = None
_locker = None

def init_driver():
    global _driver, _locker
    if _locker:
        logger.warn("Already have a locker: {1}".format(id(_locker)))
    else:
        _locker = threading.Lock()
    if _driver:
        logger.warn("Already have a driver: {1}".format(id(_driver)))
    else:
        p = Path( os.path.abspath(".") )
        p = p.joinpath("geckodrivers/geckodriver_linux_amd64")
        logger.warn("Loading driver @ " + str(p))
        #_driver = webdriver.Firefox(executable_path="/home/lizhenbo/src/mtg_buyer/geckodrivers/geckodriver_linux_amd64")
        _driver = webdriver.Firefox(executable_path=p)

def _fetch(url:str):
    global _driver, _locker
    logger.warn("id of webdriver {0}, locked with {1}".format(id(_driver), id(_locker)))
    logger.warn("fetching " + url)
    code = ""
    if _driver == None:
        init_driver()
    with _locker:
        _driver.get(url)
        code = _driver.page_source
    return code

_cache = cachetools.TTLCache(maxsize=128, ttl=3600, missing=_fetch) # 默认一小时内缓存有效

def fetch(url:str)->str:
    return _cache[url]

def clean_up_before_quit():
    global _driver, _locker
    try:
        logger.warn("killing browser driver")
        _driver.quit()
    except:
        pass
    finally:
        _driver = None
    _locker = None

if __name__ == '__main__':
    #code = fetch('http://httpbin.org/headers')
    link = "https://s.taobao.com/search?q=%E4%BA%91%E6%95%A3+%E4%B8%87%E6%99%BA%E7%89%8C&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20151211&ie=utf8&style=list"
    code = fetch(link)
    with open("/dev/shm/headers.html", "w") as fout:
        fout.write(code)
    clean_up_before_quit()
