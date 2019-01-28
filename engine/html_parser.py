import datetime, re
import requests
from bs4 import BeautifulSoup
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


def getFullPath(url, links):
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

"""
    {
        'indexSelector': '#sample > h1',
        'indexAttr': 'text',
        'selector' : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
        'startAt': 0,
        'attr' : 'data-role',
        'limit' : 0,
        'filterAttr' : 'src',
        'filterValue' : 'value',
    },
"""
def parseHtml(html, selectorDictList):
    soup = BeautifulSoup(html, 'html.parser')

    results = {}
    defaultIndex = 0

    for selectorDict in selectorDictList:
        print(selectorDictList)
        index = selectorDict.get('index', defaultIndex)
        selector = selectorDict.get('selector', '').replace("child", "of-type")
        attr = selectorDict.get('attr', 'text')
        startAt = int(selectorDict.get('startAt', '0'))
        limit = int(selectorDict.get('limit', '-1'))
        strip = selectorDict.get('strip', True)
        filterAttr = selectorDict.get('filterAttr', None)
        filterValue = selectorDict.get('filterValue', None)
    
        # Index 
        defaultIndex += 1
        
        # Select all data by selector
        searchResults = soup.select(selector)

        #Filter 있으면 필터링
        if filterAttr:
            for idx, result in enumerate(searchResults):
                if result[filterAttr] != filterValue:
                    searchResults.pop(idx)

        if limit == -1 : 
            limit = len(searchResults)

        searchResults = searchResults[startAt:limit]

        if len(searchResults) == 0:
            print("결과 없음.")
            results[index] = ''
            continue
        
        if attr == 'text':
            values = [searchResult.get_text(strip=strip) for searchResult in searchResults]
        else :
            for parentCount in range(0, attr.count(".")):
                searchResults = [searchResult.parent for searchResult in searchResults]
                attr = attr.replace(".", "", 1)
            try:
                values = [searchResult[attr] for searchResult in searchResults]
            except:
                values = ''
                print("Attribute 값이 없음.")

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

