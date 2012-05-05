import os
import sys
import nltk
from nltk.tokenize import regexp_tokenize

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def is_spanish(document):
	stopwords = nltk.corpus.stopwords.words('spanish') 
	for word in regexp_tokenize(document, "[\w#@]+"):
		if word in stopwords:
			return True
	return False

def is_french(document):
	stopwords = nltk.corpus.stopwords.words('french') 
	for word in regexp_tokenize(document, "[\w#@]+"):
		if word in stopwords:
			return True
	return False

def is_german(document):
	stopwords = nltk.corpus.stopwords.words('german') 
	for word in regexp_tokenize(document, "[\w#@]+"):
		if word in stopwords:
			return True
	return False
	
def is_dutch(document):
	stopwords = nltk.corpus.stopwords.words('dutch') 
	for word in regexp_tokenize(document, "[\w#@]+"):
		if word in stopwords:
			return True
	return False
def is_portuguese(document):
	stopwords = nltk.corpus.stopwords.words('portuguese') 
	for word in regexp_tokenize(document, "[\w#@]+"):
		if word in stopwords:
			return True
	return False
		
with open("output.txt", 'w') as dest:
	with open("step1_no_null.txt", 'r') as src:
		while 1:
			line = src.readline()					
			if not line:
				break
			# test if the line contains unicode outside ascii
			tabs = line.split('\t')
			if (not is_ascii(tabs[4])):
				continue
			if (is_spanish(tabs[4])):
				continue
			if (is_german(tabs[4])):
				continue
			if (is_french(tabs[4])):
				continue
			if (is_dutch(tabs[4])):
				continue
			if (is_portuguese(tabs[4])):
				continue
			dest.write(line.lower())
				