def getDescription(soup):
    description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if description:
        return description.get("content")

    return None