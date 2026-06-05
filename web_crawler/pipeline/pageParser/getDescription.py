def getDescription(soup):
    description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if description:
        return description.get("content")
    
    #fallback to opengraph description
    description = soup.find(
        "meta",
        attrs={"property": "og:description"}
    )

    if description:
        return description.get("content")


    return None