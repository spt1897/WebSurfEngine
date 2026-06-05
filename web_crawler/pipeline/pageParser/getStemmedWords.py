


def getStemmedWords_TF(config,appstate,soup):
    words_tf = {}
    stemmer = appstate.stemmer
    stopwords = config.stopwords
    for tag in soup(["script","style","noscript"]):
        tag.decompose()

    text = soup.get_text(separator= " ", strip=True) + " "

    cur_word=""
    for char in text:
        
        if char.isalpha():
            cur_word += char.lower()
        
        elif cur_word:
            if not cur_word in stopwords:
                cur_word = stemmer.stem(cur_word)
                words_tf[cur_word] = words_tf.get(cur_word, 0) + 1

            cur_word = ""
    
    return words_tf



    
