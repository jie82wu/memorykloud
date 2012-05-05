import nltk
from nltk.tokenize import regexp_tokenize
import math 
import collections
from operator import itemgetter 

if __name__ == '__main__':
	# preparing files for read & write
	wordsContent = open ('words.txt', 'rU')
	documentContent = open ('documents.txt', 'rU')
	numDocsContainWordContent = open('numDocsContainWord.txt', "w", 0)

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
		
	# save numDocsContainWord into a file
	for word in wordList:
		count = 0
		for documentId in documentDict.keys():
			if (word in documentDict[documentId]):
				count += 1
		numDocsContainWordContent.write("%s\t%s\n" % (word, count))