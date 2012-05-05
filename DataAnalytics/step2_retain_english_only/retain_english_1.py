import os
import sys

def is_ascii(s):
    return all(ord(c) < 128 for c in s)
	
with open("english.txt", 'w') as dest:
	with open("step1_output.txt", 'r') as src:
		while 1:
			line = src.readline()					
			if not line:
				break
			# test if the line contains unicode outside ascii
			tabs = line.split('\t')
			if (is_ascii(tabs[4])):
				dest.write(line.lower())
				