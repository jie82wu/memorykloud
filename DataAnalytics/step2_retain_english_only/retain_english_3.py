import os
import sys
from nltk.tokenize import regexp_tokenize
import re

def is_ascii(s):
    return all(ord(c) < 128 for c in s)
	
with open("english.txt", 'w') as dest:
	with open("step1_no_null.txt", 'r') as src:
		while 1:
			line = src.readline()					
			if not line:
				break
			# test if the line contains unicode outside ascii
			tabs = line.split('\t')
			if (not is_ascii(tabs[4])):
				continue
			# remove tweets that contain too few words
			words = regexp_tokenize(tabs[4].lower(), "[\w#@]+")
			remove = set([])
			for word in words:
				if re.search(r'[\d]', word) or len(word) < 4 or re.search(r'[\!\$\%\^\&\*\(\)\_\-\+\=\[\]\{\}\;\:\'\"\<\,\.\>\/\?]', word) : 
					remove.add(word)
			
			for word in remove:
				words = filter (lambda a: a != word, words)
				
			if len(set(words)) < 15:
				continue
			
			newline = ""
			for word in words:
				newline += "%s " % word
			
			dest.write("%s\t%s\n" % (tabs[0], newline))
				