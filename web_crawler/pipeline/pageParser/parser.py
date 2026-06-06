from crawler.request_page import request_page
from bs4 import BeautifulSoup
from getTitle import getTitle
from getDescription import getDescription
from getFaviconLink import getFaviconLink
from getLinks import getLinks
from getImages import getImages
from getStemmedWords import getStemmedWords_TF

#Parses the page to get title, metadata, links , text
def parseWebPage(config,appstate,workerstate,page):
    res = request_page(config, page.url)
    try:
        if res:  #successful html page request
            soup = BeautifulSoup(res.text,"html.parser")
            page.title = getTitle(soup)
            page.description = getDescription(soup)
            page.favicon_url = getFaviconLink(soup,page.url)
            page.links = getLinks(config,page.url,soup,workerstate)
            page.images= getImages(soup)
            page.words= getStemmedWords_TF(config,appstate,soup)
            return True
        
        else:
            return False
    
    except Exception as err:
        return False