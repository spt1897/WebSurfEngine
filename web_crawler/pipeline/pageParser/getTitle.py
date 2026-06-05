#Returns Title of the web paage
def getTitle(soup):
    if soup.title:
        return soup.title.get_text(strip=True)
    
    og_title= soup.find("meta",
                        attrs={"property":"og:title"}
                        )
    if og_title:
        return og_title.get("content")

    return None