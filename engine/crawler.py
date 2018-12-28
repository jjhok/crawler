import sys
import datetime, re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import logging
import pandas as pd
import asyncio

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


#### SAMPLE DATA
selectorDictList = [
    {
        'index': '작성자',
        'selector' : "#div_content > div > div.list_author > span.nickname",
        # 'attr' : 'text',
        'startAt': 1,
        # 'limit' : 13,
    },
    {
        'index': '제목',
        'selector' : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
        # 'attr' : 'data-role',
        # 'limit' : 15,
    },
    {
        'index': '작성시간',
        'selector' : "#div_content > div > div.list_time > span > span",
        'startAt' : 1,
        # 'attr' : 'data-role',
        # 'limit' : 15,
    },
]
nameSelector = "#div_content > div.board_head > div.board_name > h2 > a"
urltest = 'https://www.clien.net/service/group/allreview?&od=T31&po={pageId}'


def _bs4Login():
    pass

def _selLogin():
    pass

async def bs4SinglePage(url, selectorDictList, nameSelector=None, nameAttr='text', login=False, id=None, pwd=None):
    await sem.acquire()
    with requests.Session() as s:
        ## LOGIN
        req = await loop.run_in_executor(None, s.get, url)
        # req = s.get(url)    
        
        status = req.status_code
        header = req.headers
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')

        # Index 
        if nameSelector is not None:
            if nameAttr == 'text':
                index = soup.select(nameSelector)[0].get_text()
            else:
                index = soup.select(nameSelector)[0][nameAttr]
    
        # Content
        """
            {
                'index': 'index1',
                'selector' : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
                'startAt': 0,
                'attr' : 'data-role',
                'limit' : 0,
            },
        """
        
        results = {}
        for selectorDict in selectorDictList:
            index = selectorDict.get('index', 'unknown')
            selector = selectorDict.get('selector', '').replace("child", "of-type")
            attr = selectorDict.get('attr', 'text')
            startAt = int(selectorDict.get('startAt', '0'))
            limit = int(selectorDict.get('limit', '-1'))
            strip = selectorDict.get('strip', True)
            
            searchResults = soup.select(selector)
            if limit == -1 : 
                limit = len(searchResults)
            searchResults = searchResults[startAt:limit]
            if len(searchResults) == 0:
                print("결과 없음.")
            
            if attr == 'text':
                values = [searchResult.get_text(strip=strip) for searchResult in searchResults]
            else :
                values = [searchResult[attr] for searchResult in searchResults]
            results[index] = values

        sem.release()
        return results

def bs4GetDetailLinks(session, selector):
    pass


async def bs4GetNestedPage(url, selector, startAt = 0, limit = -1):
    selectorDictList = [
        {
            'selector' : selector,
            'startAt': 1,
            'attr' : 'href',
            'startAt': startAt,
            'limit': limit
        },
    ]
    future = bs4SinglePage(url, selectorDictList)
    rawData = await asyncio.gather(future)
    
    result = rawData[0]

    # fullpath generation
    links = result[selectorDictList[0].get('index', 'unknown')]    
    for idx, link in enumerate(links) :
        if link.startswith("http"): 
            continue
        elif link.startswith("/"):
            links[idx] = "/".join(url.split("/")[0:3]) + link
        elif link.startswith(".."):
            links[idx] = link.replace("..", "", 1)
            links[idx] = "/".join(url.split("/")[0:-2]) + link
        elif link.startswith("."):
            links[idx] = link.replace(".", "", 1)
            links[idx] = "/".join(url.split("/")[0:-1]) + link

    return links

def selSinglePage():
    pass

def selNestedPage():
    pass

def urlParse(url, variable, values):
    results = []
    for value in values:
        results.append(url.replace(variable, str(value)))
    return results

def toFile(data, filename, filetype='csv'):
    ## Todo 
    # Dict => Dataframe

    if filetype == 'csv':
        data.to_csv(filename, index=False)
    elif filetype == 'excel':
        data.to_excel(filename, index=False)
    elif filetype == 'html':
        data.to_html(filename, index=False)






async def main(urls, selectorDictList):

    futures = [bs4SinglePage(url, nameSelector=nameSelector,  selectorDictList=selectorDictList) for url in urls]
    rets = await asyncio.gather(*futures)
    
    return rets

if __name__ == "__main__":
    import time

    begin = time.time()

    ### single Thread
    # re = pd.DataFrame()
    # for url in urlParse(urltest, "{pageId}", range(0,50)):
    #     df = bs4SinglePage(url, nameSelector=nameSelector,  selectorDictList=selectorDictList)
    #     re = re.append(df)
    # print(re)

    ### multi Thread
    # loop = asyncio.get_event_loop()
    # sem = asyncio.Semaphore(10, loop=loop)
    # loop.run_until_complete(main())
    # loop.close()
    
    ###
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(10, loop=loop)

    mainpages = urlParse("https://www.clien.net/service/group/allreview?&od=T31&po={pageId}", "{pageId}", range(0,5))

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
    loop.close()

    end = time.time()
    print("Eslapsed Time : {}".format(end - begin))

