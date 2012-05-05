import nltk
from nltk.tokenize import regexp_tokenize
import math 
import collections
from operator import itemgetter 

### reference: http://groups.google.com/group/nltk-users/browse_thread/thread/2fd7b3dd241ee520
def freq(term, document): # return the term frequency in a given document
	count = 0
	for word in document:
		if (word == term):
			count += 1
	return count

def numDocsContainWord(word, documentDict):  # return the number of documents that contain the word
    count = 0 
    for documentId in documentDict.keys(): 
		if word in documentDict[documentId]:
			count += 1 
    return count 

def tf(word, document): 
    return freq(word, document) / float(len(document)) 

def idf(word, documentDict): 
	#print "%s\t%s\t%s\n" % (word, len(documentDict), float(numDocsContainWord(word, documentDict) + 1))
	return math.log10(len(documentDict)/float(numDocsContainWord(word, documentDict) + 1)) 

def tfidf(word, document, documentDict): 
	#print "%s\t tf:%s\t idf:%s \n" % (word, tf(word,document), idf(word,documentDict))
	return (tf(word,document) * idf(word,documentDict)) 

	
if __name__ == '__main__':
	# preparing files for read & write
	wordsContent = open ('words.txt', 'rU')
	documentContent = open ('documents.txt', 'rU')
	matrixContent = open('maxtrix.txt', "w", 0) 

	# read words into a wordList
	wordList = []
	for line in wordsContent:
		tabs = line.split('\t')
		wordList.append(tabs[0])
	
	# read documents into a documentDict
	documentDict = {}
	for line in documentContent:
		tabs = line.split('\t')
		documentDict[tabs[0]] = regexp_tokenize(tabs[1], "[\w'#@]+")
		
	# preparing a two dimensional dict	
	tfidfDict = collections.defaultdict(dict)
	
	# start filling the tfidf dict
	for word in wordList:
		for documentId in documentDict.keys():
			tfidfDict[documentId][word] = tfidf(word, documentDict[documentId], documentDict)
	
	# print tfidf in a file
	matrixContent.write("  ");
	for word in wordList:
		matrixContent.write("\t%s" % word)
	matrixContent.write("\n")
	
	for documentId in documentDict.keys():
		matrixContent.write("%s\t" % documentId)
		for word in wordList:
			matrixContent.write("%s\t" % tfidfDict[documentId][word])
		matrixContent.write("\n")