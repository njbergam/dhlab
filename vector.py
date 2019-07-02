# Vector Creation
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys
import wikipedia
import statistics
from scipy import stats
from nltk.tokenize.treebank import TreebankWordDetokenizer
import matplotlib.pyplot as plt
import random

from test import POSDensitySimple
from test import simpleTokenize
from test import sentenceLength
from test import cleanText

# Given a file, it will
# 	create a vector of the file's text based on certain parameters
def vectorize(fileName, firstgen):
	text = simpleTokenize(fileName)
	vector = [strength(text), avgSentenceLength(text), rebound(text, firstgen)*1000.0]
	return vector
	
def vectorize2(text, firstgen):
	vector = [strength(text), avgSentenceLength(text), rebound(text, firstgen)*1000.0]
	return vector
		
# Returns the proportion of strong words (nouns, verbs) to weak words (adj, adv)
def strength(text):
	p = POSDensitySimple(text)
	return ( float(p['NOUN']) + float(p['VERB']))/(float(p['ADJ']) + float(p['ADV']))

# Returns the average sentence length
def avgSentenceLength(text):
	s = sentenceLength(text)
	if s == []:
		return len(text)
	return statistics.mean(s)

# Returns the proportion of rebound of second/third generation wikipedia words
def rebound(text, firstgen):
	count = 0
	secgen = wikipediaWords(firstgen, 3)
	secgen = [ i[0] for i in secgen]
	thirdgen = wikipediaWords( secgen , 3)
	thirdgen = [i[0] for i in thirdgen]
	for i in range(len(text)):
		if text[i] in secgen:
			count = count +1
		if text[i] in thirdgen:
			count = count+0.5
	return count*1.0/len(text)


def cleanText(words):
	lem = WordNetLemmatizer()
	s = PorterStemmer()
	stop_words=set(stopwords.words("english"))
	filteredDict = []
	for w in words:
		if w not in stop_words and len(w)>3:
			w = lem.lemmatize(w,"v")
			#w = s.stem(w)
			filteredDict.append(w)
	return filteredDict

# Given ogWords=[yellow, fish] and numWords = 2
# [[color, orange], [gill-bearing, aquatic]]
def wikipediaWords(ogWords, numWords):
	list = []
	for i in range(len(ogWords)):
		try:
			text = nltk.Text(cleanText(nltk.word_tokenize(wikipedia.page(title = ogWords[i]).summary)))
			list.append(text[1:numWords])
		except wikipedia.exceptions.DisambiguationError as e:
			continue
			#print(ogWords[i] + " caused disambiguation error")
	return list

sf = ['time', 'suicide', 'child', 'family', 'race', 'death', 'sound','fury', 'mausoleum', 'hope', 'desire', 'harvard']
#print( vectorize('SoundAndFury.txt', sf) )
#print( vectorize2( simpleTokenize('SoundAndFury.txt'), sf) ) 


