"""
#This document will largely be walking through some of the different functions

import nltk

# Opening local text files, turning text into array of tokens
file = open("SoundAndFury.txt", "r")
words = nltk.word_tokenize(file.read())
#print(words)


# Getting most common words frequency distribution
fdist = nltk.FreqDist(words)
#print(fdist)
#print(fdist.most_common(10))


# It is very easy to plot most common words with matplotlib
import matplotlib.pyplot as plt
#fdist.plot(30,cumulative=False)
#plt.show()


# Getting useless "stop words" out of the mix (a, an, the, is, being)
from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))
#print(stop_words)
filteredDist = []
for w in words:
	if w not in stop_words:
		filteredDist.append(w)
print(nltk.FreqDist(filteredDist).most_common(10))

"""

import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
# This function should, given a fileName, 1) tokenize the text file 
# 2) remove three or fewer characters, 3) Removing stopwords
# 4) Lemmatization (third person-->first person, past to present tense)
# 5) Stemming (root form of word)
# Return the tokenized array
def cleanText(fileName):
	lem = WordNetLemmatizer()
	stem = PorterStemmer()
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	stop_words=set(stopwords.words("english"))
	filteredDict = []
	for w in words:
		if w not in stop_words and len(w)>3:
			w = lem.lemmatize(w,"v")
			filteredDict.append(w)
	return filteredDict
	
print( cleanText("SoundAndFury.txt") )


# Returns a dictionary with the density
def POSDensity()


		