import nltk
from nltk.tokenize import regexp_tokenize
import math 
import collections
from operator import itemgetter 

if __name__ == '__main__':
	content = open ('step2_english_3.txt','rU')
	output = open('wordlist.txt', "w", 0) 

	# read documents into a documentList
	documentList = []
	for line in content:
		tabs = line.split('\t')
		documentList.append(tabs[1].lower())
	
	stopwords = nltk.corpus.stopwords.words('english') 
	words = {}
	for document in documentList:
		for word in regexp_tokenize(document, "[\w#@]+"):	# we define ours words to contain ', # and @
			if word not in stopwords and not word.isdigit() and len(word) > 2: 
				words[word] = words.get(word, 0) + 1
	
	for item in sorted(words.items(), key=itemgetter(1), reverse=True): 
		if (item[1] < 6):
			break
		output.write ("%s\t%s\n" % (item[0], item[1]))