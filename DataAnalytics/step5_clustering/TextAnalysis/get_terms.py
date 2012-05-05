import nltk
from nltk.tokenize import regexp_tokenize
from operator import itemgetter 

if __name__ == '__main__':
	content = open ('10.txt','rU')
	output = open('wordlist10.txt', "w", 0) 

	words = {}
	for line in content:
		for word in regexp_tokenize(line, "[\w#@]+"):	# we define ours words to contain ', # and @
				words[word] = words.get(word, 0) + 1
	
	for item in sorted(words.items(), key=itemgetter(1), reverse=True): 
		output.write ("%s\t%s\n" % (item[0], item[1]))