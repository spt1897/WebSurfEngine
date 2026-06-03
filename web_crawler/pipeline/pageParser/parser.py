from crawler.request_page import request_page
from bs4 import BeautifulSoup
from getTitle import getTitle
from getDescription import getDescription
from getFaviconLink import getFaviconLink
from getLinks import getLinks
from getStemmedWords import getStemmedWords

#Parses the page to get title, metadata, links , text
def parseWebPage(config,page):
    res = request_page(config, page.url)
    if res:  #successful html page request
        soup = BeautifulSoup(res.text,"html.parser")
        page.title = getTitle(soup)
        page.description = getDescription(soup)
        page.favicon_url = getFaviconLink(soup,page.url)
        page.links = getLinks(soup)
        page.words= getStemmedWords(soup)
        