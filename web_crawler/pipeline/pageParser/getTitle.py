#Returns Title of the web paage
def getTitle(soup):
    if soup.title:
        return soup.title.get_text(strip=True)

    return None