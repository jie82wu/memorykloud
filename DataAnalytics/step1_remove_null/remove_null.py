import os
import sys

rootdir = sys.argv[1]

for folder, subs, files in os.walk(rootdir):
    with open(os.path.join(folder,'python-outfile.txt'), 'w') as dest:
        for filename in files:
            with open(os.path.join(folder, filename), 'r') as src:
				while 1:
					line = src.readline()					
					if not line:
						break
					tabs = line.split('\t')
					if (tabs[3] != "null"):
						dest.write(line)
                