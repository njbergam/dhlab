import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter

# Getting the text, converting and cleaning
from test import cleanText
words = cleanText("CatcherSalinger.txt")

import matplotlib.pyplot as plt


# Word Frequency plot
def freqPlot(words):
	fdist = nltk.FreqDist(words)
	fdist.plot(30,cumulative=False)
	plt.show()
	
# Sentence Length Histogram
from test import sentenceLength
#def senPlot(words):


# STUDY ON SHORT STORIES
import sys
from test import simpleTokenize

# Generates an array of words that are found in the same context
# as a chosen array of words
def generateSimilarWords(rootTextName, newDocName, words):
	text = nltk.Text(word.lower() for word in simpleTokenize(rootTextName) )
	sys.stdout = open(newDocName, 'w')
	for i in range(len(words)):
		print(words[i])
		text.similar(words[i])
		print()
	return cleanText(newDocName)

# Banana Fish
bw = ['yellow', 'fish', 'glass', 'day', 'perfect', 'foot', 'beach']
#bwArray = simpleTokenize( generateSimilarWords("CatcherSalinger.txt", "bananaWords.txt", bw) )

# Teddy 
tw = ['teddy', 'poet', 'gift horse', 'nephritis', 'spritual', 'diary', 'orphan', 'triumvirate', 'myriad' ]
#generateSimilarWords("CatcherSalinger.txt", "teddyWords.txt", tw)


def wordProgression(words, word):
    occurences = []
    section = list(range(100))
    ocount = 0
    i = 0
    print (len(words))
    while i < len(words):
        j = i
        while i < j + 100 and i < len(words):
            if words[i] == word:
                ocount += 1
            i += 1
        occurences.append(ocount)
        ocount = 0
    return occurences

t = nltk.Text(word.lower() for word in simpleTokenize("CatcherSalinger.txt"))
y = wordProgression( t , "glass")
x =  list(range( int(len(t)/100) +1))

plt.plot(x,y)
plt.show()
