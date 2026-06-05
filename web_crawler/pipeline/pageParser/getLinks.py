from urllib.parse import urljoin

def getLinks(config,url,soup, workerstate):
    links =[]
    seenPageLinks = set()
    for a in soup.find_all("a",href=True):
        if len(links)>=config.LINKS_PER_PAGE:
            break

        link =urljoin(url,a["href"])
        if(not workerstate.redis_client.sismember("visited_urls",link) 
                and not link in seenPageLinks
                and (link.startswith("https://") or link.startswith("http://"))):
            links.append(link)
            seenPageLinks.add(link)

    return links