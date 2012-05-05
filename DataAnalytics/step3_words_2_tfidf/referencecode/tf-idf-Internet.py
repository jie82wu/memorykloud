import nltk 
import math 
from operator import itemgetter 
from nltk.corpus import reuters 

def freq(word, document): 
    return reuters.words(document).count(word) 

def docLen(document): 
    return len(reuters.words(document)) 

def numDocsContainWord(word, documentList): 
    count = 0 
    for document in documentList: 
        if freq(word, document) > 0: 
            count += 1 
    return count 

def tf(word, document): 
    return freq(word, document) / float(docLen(document)) 

def idf(word, documentList): 
    return math.log(len(documentList)/numDocsContainWord(word, documentList)) 

def tfidf(word, document, documentList): 
    return (tf(word,document) * idf(word,documentList)) 


if __name__ == '__main__': 
    documentList = [f for f in reuters.fileids(categories='acq') if f.startswith("train")] 
    stopwords = nltk.corpus.stopwords.words('english') 
    words = {} 
    for document in documentList: 
        for word in reuters.words(document): 
            if word.lower() not in stopwords and word.isalnum(): 
                words[word] = tfidf(word,document,documentList) 
    for item in sorted(words.items(), key=itemgetter(1), 
reverse=True): 
        print "%f <= %s" % (item[1], item[0])[:50] 