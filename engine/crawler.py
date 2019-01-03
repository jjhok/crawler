import datetime, re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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


### Chrome DRIVER 
CHROME_DRIVER = '/Users/1001078/Documents/workspace/Python/crawler/engine/chromedriver_mac'

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



def _getFullPath(url, links):
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

def _parseHtml(html, selectorDictList, nameSelector=None, nameAttr='text'):
    soup = BeautifulSoup(html, 'html.parser')

    # Index 
    if nameSelector is not None:
        if nameAttr == 'text':
            index = soup.select(nameSelector)[0].get_text()
        else:
            index = soup.select(nameSelector)[0][nameAttr]
    
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
            raise Exception("결과 없음.")
        
        if attr == 'text':
            values = [searchResult.get_text(strip=strip) for searchResult in searchResults]
        else :
            values = [searchResult[attr] for searchResult in searchResults]
        results[index] = values

    return results


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


# LoginData Sample
"""
    {
        'nameAttr_of_inputTag': 'value',
        'nameAttr_of_inputTag': 'value',
    },
"""
def bs4Login(loginActionUrl, loginData):
    session = requests.Session()
    req = session.post(loginActionUrl, data=loginData)
    if req.status_code == 200:
        return session
    else :
        raise Exception("로그인 실패")


def selLogin(loginUrl, idXpath, id, pwdXpath, pwd, submitXpath):
    # driver = webdriver.Chrome('chromedriver_mac')
    driver = webdriver.Chrome(CHROME_DRIVER)
    driver.implicitly_wait(3)

    driver.get(loginUrl)
    driver.find_element_by_xpath(idXpath).send_keys(id)
    driver.find_element_by_xpath(pwdXpath).send_keys(pwd)
    driver.find_element_by_xpath(submitXpath).click()

    return driver


async def bs4GetNestedPage(url, selector, startAt = 0, limit = -1, loginSession=None):
    selectorDictList = [
        {
            'selector' : selector,
            'startAt': 1,
            'attr' : 'href',
            'startAt': startAt,
            'limit': limit
        },
    ]
    future = bs4SinglePage(url, selectorDictList, loginSession=loginSession)
    rawData = await asyncio.gather(future)
    
    result = rawData[0]

    # fullpath generation
    links = result[selectorDictList[0].get('index', 'unknown')]    
    return _getFullPath(url, links)


async def selNestedPage(url, selector, startAt=0, limit=-1, driver=None, waitingForXpath=None, delay=3):
    await sem.acquire()

    selectorDictList = [
        {
            'selector' : selector,
            'startAt': 1,
            'attr' : 'href',
            'startAt': startAt,
            'limit': limit
        },
    ]

    if driver is None :   
        driver = webdriver.Chrome(CHROME_DRIVER)
        driver.implicitly_wait(3)

    driver.get(url)
    
    if waitingForXpath is not None:
        try:
            state = EC.presence_of_element_located((By.XPATH, waitingForXpath))
            WebDriverWait(driver, delay).until(state)
            print("Document is ready")
        except TimeoutException:
            print("Time out")

    html = driver.page_source

    result = _parseHtml(html, selectorDictList)

    sem.release()
    driver.close()
    
    links = result[selectorDictList[0].get('index', 'unknown')]    
    return _getFullPath(url, links)



# selectorDictList Sample
"""
    {
        'index': 'index1',
        'selector' : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
        'startAt': 0,
        'attr' : 'data-role',
        'limit' : 0,
    },
"""
async def bs4SinglePage(url, selectorDictList, nameSelector=None, nameAttr='text', loginSession=None):
    await sem.acquire()

    if loginSession is None :
        s = requests.Session()
    else :
        s = loginSession

    req = await loop.run_in_executor(None, s.get, url)
    # req = s.get(url)    
    
    status = req.status_code
    header = req.headers
    html = req.text

    sem.release()

    return _parseHtml(html, selectorDictList, nameSelector=nameSelector, nameAttr=nameAttr)



async def selSinglePage(url, selectorDictList, nameSelector=None, nameAttr='text', driver=None, waitingForXpath=None, delay=3):
    await sem.acquire()

    if driver is None :   
        driver = webdriver.Chrome(CHROME_DRIVER)
        driver.implicitly_wait(3)

    driver.get(url)
    

    if waitingForXpath is not None:
        try:
            state = EC.presence_of_element_located((By.XPATH, waitingForXpath))
            WebDriverWait(driver, delay).until(state)
            print("Document is ready")
            driver.scroll
        except TimeoutException:
            print("Time out")

    html = driver.page_source

    result = _parseHtml(html, selectorDictList, nameSelector=nameSelector, nameAttr=nameAttr)

    sem.release()
    driver.close()

    return result
    
 




async def main(urls, selectorDictList):

    futures = [bs4SinglePage(url, nameSelector=nameSelector,  selectorDictList=selectorDictList) for url in urls]
    rets = await asyncio.gather(*futures)
    
    return rets

if __name__ == "__main__":
    import time

    begin = time.time()

    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(10, loop=loop)

    ## BS4 Login wiki TEST
    # loginData = {
    #     'os_username': '1001078',  # input Tag > name attribute
    #     'os_password' : "jjhok6757!",
    #     'os_destination' : "/index.action",
    # }

    # loginActionUrl = "http://wiki.skplanet.com/dologin.action"
    # loginSession = _bs4Login(loginActionUrl, loginData)

    # ## Detail Page list
    # detailLinks = loop.run_until_complete(bs4GetNestedPage("http://wiki.skplanet.com/admin/originaltheme/organizer.action", selector="#rw_uncategorized_container > div > div.rw_item_body > ul > li > span.rw_item_content > span.rw_actions > a", loginSession=loginSession))
    # print(detailLinks)
    


    ### BS4 clien.net TEST 
    # mainpages = urlParse("https://www.clien.net/service/group/allreview?&od=T31&po={pageId}", "{pageId}", range(0,2))

    # async def sample(mainpages):
    #     futures = [bs4GetNestedPage(url, "#div_content > div > div.list_title > a.list_subject", startAt=1) for url in mainpages]
    #     rets = await asyncio.gather(*futures)
    #     rets = [flatItem for itemOfList in rets for flatItem in itemOfList]
    #     return rets
        
    # pages = loop.run_until_complete(sample(mainpages))
    # print(len(pages))

    # selectorDictList = [
    #     {
    #         'index': 'IP',
    #         'selector': '#div_content > div.post_view > div.post_author > span:nth-child(2)',

    #     }
    # ]

    # ips = loop.run_until_complete(main(pages, selectorDictList))
    # print(ips)
    # df = pd.DataFrame(ips)
    # print(df)

    ### SELENIUM Login wiki Test
    loginUrl = "http://wiki.skplanet.com/login.action?os_destination=%2Findex.action&permissionViolation=true"
    driver = selLogin(loginUrl, '//*[@id="os_username"]', '********', '//*[@id="os_password"]', '********', '//*[@id="loginButton"]')

    url = "http://wiki.skplanet.com/admin/originaltheme/organizer.action"
    selectorDictList = [
        {
            'index': 'Space 이름',
            'selector': '#rw_uncategorized_container > div > div.rw_item_body > ul > li > span.rw_item_content',
        },
        {
            'index': 'UNCATEGORIZED',
            'selector': '#rw_uncategorized_container > div > div.rw_item_body > ul > li > span.rw_item_content > span.rw_actions > a',
            'attr': 'href'
        }
    ]
    # result = loop.run_until_complete(selNestedPage(url, selector='#rw_uncategorized_container > div > div.rw_item_body > ul > li > span.rw_item_content > span.rw_actions > a', driver=driver, waitingForXpath='//*[@id="rw_uncategorized_container"]/div/div'))
    result = loop.run_until_complete(selSinglePage(url, selectorDictList=selectorDictList, driver=driver, waitingForXpath='//*[@id="rw_uncategorized_container"]/div/div'))
    df = pd.DataFrame(result)
    print(df)
    toFile(df, 'wiki.csv')

    loop.close()

    end = time.time()
    print("Eslapsed Time : {}".format(end - begin))

