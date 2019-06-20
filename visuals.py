import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys
from test import simpleTokenize

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
def senLen(text):
	s = sentenceLength(text)
	plt.plot(list(range(len(s))), s) 


# STUDY ON SHORT STORIES

# Generates an second generation of words, based on the context in rootTextNae
# and a given array of first gen words picked out by human reading. 
def generateSimilarWords(rootTextName, newDocName, words):
	text = nltk.Text(word.lower() for word in simpleTokenize(rootTextName) )
	sys.stdout = open(newDocName, 'w')
	for i in range(len(words)):
		print(words[i])
		text.similar(words[i], 1)
		print()
	sys.stdout = sys.__stdout__
	m = simpleTokenize(newDocName)
	n = m.copy()
	for i in range(len(m)):
		if m[i] == "No" and m[i+1] == "matches":
			n.remove("No")
			n.remove("matches")
	return n

# Banana Fish
bw = ['yellow', 'fish', 'glass', 'foot', 'beach', 'suicide']
bwArray = generateSimilarWords("CatcherSalinger.txt", "bananaWords.txt", bw) 

# Teddy 
tw = ['teddy', 'poet', 'gift horse', 'nephritis', 'spritual', 'diary', 'orphan', 'triumvirate', 'myriad' ]
twArray = generateSimilarWords("CatcherSalinger.txt", "teddyWords.txt", tw)

# The Laughing Man
lw = ['chief','museum', 'baseball', 'laugh', 'descendant']
lwArray = generateSimilarWords("CatcherSalinger.txt", "laughingWords.txt", tw)

# For Esme – With Love and Squalor
ew = ['esme', 'love', 'squalor', 'wedding', 'faculties', 'war']
ewArray = generateSimilarWords("CatcherSalinger.txt", "esmeWords.txt", tw)

# Given a text as an array of words, takes in a first and sec gen words
# and outputs the frequencies of words within that wordlist
# Each entry in the list represents the frequency in consecutive
# hundred words
def wordProgression(words, firstgen, secgen):
    occurences = []
    section = list(range(100))
    ocount = 0
    i = 0
    while i < len(words):
        j = i
        while i < j + 100 and i < len(words):
            if words[i] in firstgen:
                ocount += 4
            elif words[i] in secgen:
            	ocount += 1
            i += 1
        occurences.append(ocount)
        ocount = 0
    return occurences




fig, axs = plt.subplots(4)
fig.suptitle('Short Story Readings on Salinger')

def plotChronoMap(textName, firstgen, secgen, title, graphNum):
	t = nltk.Text(word.lower() for word in simpleTokenize(textName))
	y = wordProgression( t , firstgen, secgen)
	x =  list(range( int(len(t)/100) +1))
		# If you want to make separate plots
		#a, f = plt.subplots(1)
		#a.suptitle(title)
		#f.plot(x,y)
	axs[graphNum].plot(x, y)
	axs[graphNum].set_title(title)

plotChronoMap("CatcherSalinger.txt", bw, bwArray, "Bananafish Words in Catcher", 0)
plotChronoMap("CatcherSalinger.txt", tw, twArray, "Teddy Words in Catcher", 1)
plotChronoMap("CatcherSalinger.txt", lw, lwArray, "Laughing Man Words in Catcher", 2)
plotChronoMap("CatcherSalinger.txt", ew, ewArray, "Esme Words in Catcher", 3)

#uniform_data = np.random.rand(1, 1)
#axs[2] = sns.heatmap(uniform_data, linewidth=0.5)
plt.tight_layout()
plt.show()
