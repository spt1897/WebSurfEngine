
def tokenize_by_freq(text,stopwords,stemmer):
    words_tf ={}
    cur_word=""
    for char in text+" ":
        
        if char.isalnum():
            cur_word += char.lower()
        
        elif cur_word:
            if not cur_word in stopwords:
                cur_word = stemmer.stem(cur_word)
                words_tf[cur_word] = words_tf.get(cur_word, 0) + 1

            cur_word = ""

    return words_tf