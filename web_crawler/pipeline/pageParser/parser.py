from web_crawler.pipeline.crawler.request_page import request_page
from bs4 import BeautifulSoup
from web_crawler.pipeline.pageParser.getTitle import getTitle
from web_crawler.pipeline.pageParser.getDescription import getDescription
from web_crawler.pipeline.pageParser.getFaviconLink import getFaviconLink
from web_crawler.pipeline.pageParser.getLinks import getLinks
from web_crawler.pipeline.pageParser.getImages import getImages
from web_crawler.pipeline.pageParser.getStemmedWords import getStemmedWords_TF

#Parses the page to get title, metadata, links , text
def parseWebPage(config,appstate,workerstate,page):
    res = request_page(config, page.url)
    try:
        if res:  #successful html page request
            soup = BeautifulSoup(res.text,"html.parser")
            page.title = getTitle(soup) or ""
            page.description = getDescription(soup) or ""
            page.favicon_url = getFaviconLink(soup,page.url)
            page.links = getLinks(config,page.url,soup,workerstate)
            page.images= getImages(config,appstate,soup,page.url)
            page.stemmedWords_TF= getStemmedWords_TF(config,appstate,soup)
            return True
        
        else:
            appstate.msg_queue.put(("ERROR","",f"Failed at fetching page:{page.url}"))
            return False
    
    except Exception as err:
        appstate.msg_queue.put(("ERROR","",f"Failed at data extraction : {err}"))
        return False