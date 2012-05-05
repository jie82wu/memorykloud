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

def tf(word, document): 
    return freq(word, document) / float(len(document)) 

	
if __name__ == '__main__':
	# preparing files for read & write
	numDocsContainWordContent = open ('numDocsContainWord.txt', 'rU')
	documentContent = open ('documents.txt', 'rU')
	matrixContent = open('maxtrix.txt', "w", 0) 

	# read words into a wordDict
	wordDict = {}
	for line in numDocsContainWordContent:
		tabs = line.split('\t')
		wordDict[tabs[0]] = float(tabs[1])
	
	# read documents into a documentDict
	documentDict = {}
	for line in documentContent:
		tabs = line.split('\t')
		documentDict[tabs[0]] = regexp_tokenize(tabs[1], "[\w'#@]+")
		
	# print tfidf in a file
	matrixContent.write("  ");
	for word in wordDict.keys():
		matrixContent.write("\t%s" % word)
	matrixContent.write("\n")
	
	numDocs = len(documentDict)
	counter = 0
	for documentId in documentDict.keys():
		counter += 1
		print "%s\n" % (counter)
		matrixContent.write("%s\t" % documentId)
		for word in wordDict.keys():
			tfvalue = tf(word,documentDict[documentId])
			idfvalue = math.log10(numDocs /float(wordDict[word] + 1))
			#print "%s\t%s" % (word, str(tfvalue*idfvalue))
			matrixContent.write("%s\t" %  str(tfvalue*idfvalue) )
		matrixContent.write("\n")