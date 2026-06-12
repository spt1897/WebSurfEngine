from web_crawler.pipeline.pageParser.tokenizer import tokenize_by_freq


def getStemmedWords_TF(config,appstate,soup):
    stemmer = appstate.stemmer
    stopwords = config.stopwords
    for tag in soup(["script","style","noscript"]):
        tag.decompose()

    text = soup.get_text(separator= " ", strip=True)

    cur_word=""
    
    return tokenize_by_freq(text, stopwords, stemmer)



    
