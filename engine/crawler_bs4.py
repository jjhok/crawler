import datetime, re
import requests
import logging
import pandas as pd
import asyncio
from bs4 import BeautifulSoup
import json
from .html_parser import *

## LOGGING setup
myLogger = logging.getLogger("my")
myLogger.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s - %(asctime)s] %(message)s')
# stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler('crawler.log')
file_handler.setFormatter(formatter)
# myLogger.addHandler(stream_handler)
myLogger.addHandler(file_handler)


def bs4Connect(url, test=True):
    session = requests.Session()
    try : 
        res = session.get(url)
        if test == True:
            return {"STATUS_CODE": res.status_code, "response": res.text}
    except Exception as ex:
        if test == True:
            return {"ERROR": "{}".format(ex)}
        else :
            return None


# LoginData Sample
"""
    {
        'nameAttr_of_inputTag': 'value',
        'nameAttr_of_inputTag': 'value',
        'validate_selctor': 'selector',
    },
"""
def bs4Login(loginActionUrl, inputDict, test=False):
    session = requests.Session()
    try: 
        res = session.post(loginActionUrl, data=inputDict)
    except Exception as ex:
        if test == True:
            return {"ERROR": "{}".format(ex)}
        else :
            return None

    if test == True:
        if res.status_code == 200:
            selectorDictList = [{        
                'selector' : inputDict.get('validate_selector', ''),
            }]
            result = parseHtml(res.text, selectorDictList)
            return {"STATUS_CODE": res.status_code, "response": json.dumps(result, ensure_ascii=False)}   ### ensure_ascii 한글깨짐
        else :
            return {"STATUS_CODE": res.status_code, "response": "ERROR"}
    else:
        if res.status_code == 200:
            return session
        else :
            raise Exception("로그인 실패")

async def bs4GetNestedPage(loop, sem, url, selector, startAt = 0, limit = -1, loginSession=None):
    selectorDictList = [
        {
            'selector' : selector,
            'startAt': 1,
            'attr' : 'href',
            'startAt': startAt,
            'limit': limit
        },
    ]
    future = bs4SinglePage(loop, sem, url, selectorDictList, loginSession=loginSession)
    rawData = await asyncio.gather(future)
    
    result = rawData[0]
    
    # fullpath generation
    links = result[selectorDictList[0].get('index', 0)]    
    return getFullPath(url, links)


# selectorDictList Sample
"""
    {
        'index': 'index1',
        'selector' : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
        'startAt': 0,
        'attr' : 'data-role',
        'limit' : 0,
        'filterAttr' : 'src',
        'filterValue' : 'value',
    },
"""
async def bs4SinglePage(loop, sem, url, selectorDictList, nameSelector=None, nameAttr='text', loginSession=None, driverForCookie=None):
    await sem.acquire()

    if loginSession is not None :
        s = loginSession
    elif driverForCookie is not None:
        s = requests.Session()
        cookie = [s.cookies.set(c['name'], c['value']) for c in driverForCookie.get_cookies()]
    else :
        s = requests.Session()
        

    req = await loop.run_in_executor(None, s.get, url)
    # req = s.get(url)    
    
    status = req.status_code
    header = req.headers
    html = req.text

    sem.release()

    return parseHtml(html, selectorDictList)




async def main(urls, selectorDictList, nameSelector=None, loginSession=None, driverForCookie=None, driver=None, waitingForXpath=None):
    futures = [bs4SinglePage(url, nameSelector=nameSelector,  selectorDictList=selectorDictList, loginSession=loginSession) for url in urls]
    rets = await asyncio.gather(*futures)
    return rets

if __name__ == "__main__":
    import time

    begin = time.time()

    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(10, loop=loop)

    ## BS4 Login wiki TEST
    # loginData = {
    #     'os_username': '100XXXX',  # input Tag > name attribute
    #     'os_password' : "********",
    #     'os_destination' : "/index.action",
    #     'validate_selector': 'selector...'
    # }

    # loginActionUrl = "http://wiki.skplanet.com/dologin.action"
    # loginSession = bs4Login(loginActionUrl, loginData)

    # ## Detail Page list
    # detailLinks = loop.run_until_complete(bs4GetNestedPage("http://wiki.skplanet.com/admin/originaltheme/organizer.action", selector="#rw_uncategorized_container > div > div.rw_item_body > ul > li > span.rw_item_content > span.rw_actions > a", loginSession=loginSession))
    # print(detailLinks)

    ### BS4 clien.net TEST 
    mainpages = urlParse("https://www.clien.net/service/group/allreview?&od=T31&po={pageId}", "{pageId}", range(0,2))

    async def sample(mainpages):
        futures = [bs4GetNestedPage(url, "#div_content > div > div.list_title > a.list_subject", startAt=1) for url in mainpages]
        rets = await asyncio.gather(*futures)
        rets = [flatItem for itemOfList in rets for flatItem in itemOfList]
        return rets
        
    pages = loop.run_until_complete(sample(mainpages))
    print(len(pages))

    selectorDictList = [
        {
            'index': 'IP',
            'selector': '#div_content > div.post_view > div.post_author > span:nth-child(2)',

        }
    ]

    ips = loop.run_until_complete(main(pages, selectorDictList))
    print(ips)
    df = pd.DataFrame(ips)
    print(df)
    toFile(df, 'wiki.csv')

    loop.close()

    end = time.time()
    print("Eslapsed Time : {}".format(end - begin))

