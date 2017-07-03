from selenium import webdriver
import threading
import cachetools
import logging
from pathlib import Path, PurePosixPath
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
        import platform
        _system = platform.system()
        epath = "" 
        #https://github.com/mozilla/geckodriver/releases
        p = Path(".")
        p = p.joinpath("geckodrivers")
        if _system == "Windows":
            p = p.joinpath("geckodriver-v0.14.0-win64.exe")
     #       geckodriver-v0.14.0-win64
            #print(p.resolve())
            import os.path
            #print(os.path)
            p=p.resolve()
            epath = str( p  )
            #epath = epath.replace("\\", "\\\\")
            #print( os.path.basename(epath))
            #print(epath)
            #epath = "/c/Users/step_/Documents/mtg_buyer/geckodrivers/geckodriver-v0.14.0-win64.exe"
            from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
            bin = FirefoxBinary(epath)
            #_driver = webdriver.Firefox(firefox_binary=bin)#, executable_path=p0)
            epath = "/c/Users/step_/Documents/mtg_buyer/geckodrivers"
            epath = r'C:\Users\step_\Documents\mtg_buyer\geckodrivers\geckodriver.exe'
            _driver = webdriver.Firefox(executable_path=epath)
        else:
            logger.warn("hack for Linux")
            epath = "/home/lizhenbo/src/mtg_buyer/geckodrivers/geckodriver_linux_amd64"
            _driver = webdriver.Firefox(executable_path=epath)


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
    init_driver()
    #code = fetch('http://httpbin.org/headers')
    link = "https://s.taobao.com/search?q=%E4%BA%91%E6%95%A3+%E4%B8%87%E6%99%BA%E7%89%8C&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20151211&ie=utf8&style=list"
    code = fetch(link)
    #with open("/dev/shm/headers.html", "w") as fout:
    with open(r'C:\Users\step_\Documents\mtg_buyer\headers.html', "w", encoding="utf-8") as fout:
        fout.write(code)
    clean_up_before_quit()
