import nltk
from nltk.tokenize import regexp_tokenize
import math 
import collections
from operator import itemgetter 

### reference: http://groups.google.com/group/nltk-users/browse_thread/thread/2fd7b3dd241ee520
def freq(term, document): # return the term frequency in a given document
	count = 0
	for word in regexp_tokenize(document, "[\w'#@]+"):
		if (word == term):
			count += 1
	return count

def docLen(document): # return the num of words in a document
    return len(regexp_tokenize(document, "[\w'#@]+")) 

def numDocsContainWord(word, documentList):  # return the number of documents that contain the word
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
	content = open ('sample.txt','rU')
	output = open('output.txt', "w", 0) 

	# read documents into a documentList
	documentDict = {}
	documentList = []
	for line in content:
		tabs = line.split('\t')
		documentDict[tabs[0]] = tabs[4].lower()
		documentList.append(tabs[4].lower())
	
	stopwords = nltk.corpus.stopwords.words('english') 
	words = collections.defaultdict(dict)
	for documentId, document in documentDict.items():
		for word in regexp_tokenize(document, "[\w'#@]+"):	# we define ours words to contain ', # and @
			if word.lower() not in stopwords and not word.isdigit(): 
				words[word][documentId] = tfidf(word,document,documentList) 
	
	output.write("  ");
	for documentId in documentDict.keys():
		output.write("\t%s" % documentId)
	output.write("\n")
	for word, documenthash in words.items():
		output.write("%s\t" % word)
		for documentId, document in documentDict.items():
			if documentId in words[word]:
				output.write("%s\t" % words[word][documentId])
			else:
				output.write("0\t" )
		output.write("\n")