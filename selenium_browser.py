from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import threading
import cachetools
import logging
logger = logging.getLogger(__name__)

#https://coderwall.com/p/9jgaeq/set-phantomjs-user-agent-string
#_dcap = dict(DesiredCapabilities.PHANTOMJS)
#_dcap["phantomjs.page.settings.userAgent"] = (
    #"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"
#)
#_driver = webdriver.PhantomJS(desired_capabilities=_dcap)
#_driver = webdriver.PhantomJS()
try:
    _driver = webdriver.Firefox()
except:
    logger.warn("hack for Linux")
    _driver = webdriver.Firefox(executable_path="/home/lizhenbo/src/mtg_buyer/geckodriver")
_locker = threading.Lock()

def _fetch(url:str):
    logger.warn("id of webdriver %d" % id(_locker))
    logger.warn("fetching " + url)
    code = ""
    with _locker:
        _driver.get(url)
        code = _driver.page_source
    return code

_cache = cachetools.TTLCache(maxsize=128, ttl=3600, missing=_fetch) # 默认一小时内缓存有效

def fetch(url:str)->str:
    return _cache[url]

def clean_up_before_quit():
    try:
        logger.warn("killing browser driver")
        _driver.quit()
    except:
        pass

if __name__ == '__main__':
    #code = fetch('http://httpbin.org/headers')
    link = "https://s.taobao.com/search?q=%E4%BA%91%E6%95%A3+%E4%B8%87%E6%99%BA%E7%89%8C&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20151211&ie=utf8&style=list"
    code = fetch(link)
    with open("/dev/shm/headers.html", "w") as fout:
        fout.write(code)
