import nltk
from nltk.tokenize import regexp_tokenize
import math
from operator import itemgetter 

if __name__ == '__main__':
	file1 = open ('hash4.txt','rU')
	file2 = open ('hash10.txt','rU')
	output = open('difference.txt', "w", 0) 

	wordDict1 = {}
	for line in file1:
		tabs = line.split('\t')
		wordDict1[tabs[0]] = float(tabs[1])
	
	wordDict2 = {}
	for line in file2:
		tabs = line.split('\t')
		wordDict2[tabs[0]] = float(tabs[1])
		
	mergedSet = set(wordDict1.keys()).union(set(wordDict2.keys()))
	
	wordDiff = {}
	for word in mergedSet:
		wordDiff[word] = (wordDict1.get(word, 0) - wordDict2.get(word, 0)) / (wordDict1.get(word, 0) + wordDict2.get(word, 0))
	
	for item in sorted(wordDiff.items(), key=itemgetter(1), reverse=True): 
		if (math.fabs(item[1]) > 0.1) and (wordDict1.get(item[0],0) > 1) and (wordDict2.get(item[0],0) > 1):
			output.write ("%s\t%s\n" % (item[0], item[1]))
		