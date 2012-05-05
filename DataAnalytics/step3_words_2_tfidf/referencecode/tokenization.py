import nltk 
from nltk.draw.plot_graph import plot, Marker
from nltk.probability import SimpleFreqDist

# Extract a list of words from the corpus
corpus = open('sample.txt').read() 
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
tokens = tokenizer().tokenize(corpus) 

# Construct a frequency distribution of word lengths
wordlen_freqs = SimpleFreqDist()
for token in tokens:
    wordlen_freqs.inc(len(token.type()))

# Exctract the set of word lengths found in the corpus
wordlens = wordlen_freqs.samples()

# Construct a list of (wordlen, count) and plot the results.
points = [(wordlen, wordlen_freqs.count(wordlen))
          for wordlen in wordlens]
plot(Marker(points))