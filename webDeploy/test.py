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



# Getting useless "stop words" out of the mix (a, an, the, is, being)


"""

"""
Names Of Salinger Stories


A Perfect Day for Bananafish

Uncle Wiggily in Connecticut

Just Before the War with the Eskimos

The Laughing Man

Down at the Dinghy

For Esme:--with Love and Squalor

Pretty Mouth and Green Eyes

De Daumier-Smith's Blue Period

Teddy
"""



import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
from nltk.tokenize.treebank import TreebankWordDetokenizer
import statistics
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords


# This function should, given a fileName, 1) tokenize the text file
# 2) remove three or fewer characters, 3) Removing stopwords
# 4) Lemmatization (third person-->first person, past to present tense)
# 5) Stemming (root form of word)
# Return the tokenized array
def cleanText(fileName):
	lem = WordNetLemmatizer()
	s = PorterStemmer()
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	stop_words=set(stopwords.words("english"))
	filteredDict = []
	for w in words:
		if w not in stop_words and len(w)>3:
			w = lem.lemmatize(w,"v")
			#w = s.stem(w)
			filteredDict.append(w)
	return filteredDict

def deList(str):
	str = str.replace(" ", "")
	return str.split(",")

# Given a filename, returns an array of tokens (words, punctuation are separated)
def simpleTokenize(fileName):
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	return words

def detokenize(text):
	return TreebankWordDetokenizer().detokenize(text)

def saveTopWords(text, title):

	counts = Counter(text)
	labels, values = zip(*counts.items())
	# sort your values in descending order
	indSort = np.argsort(values)[::-1]
	# rearrange your data
	labels = np.array(labels)[indSort][0:20]
	values = np.array(values)[indSort][0:20]
	indexes = np.arange(len(labels))

	bar_width = 0.35

	plt.bar(indexes, values)

	# add labels
	plt.xticks(indexes + bar_width, labels, rotation='vertical')

	plt.savefig('templates/static/graphs/' + title + '.png')
	plt.close()








# Returns a dictionary with the proportions of different types of speech
# This uses simplified tags, so it only contains nouns, verbs, adjectives, pronouns, and adverbs
def POSDensitySimple(array):
	tagged = nltk.pos_tag(array);
	simplifiedTags = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in tagged]
	s = len(array)
	counts = dict( Counter(tag for word, tag in simplifiedTags))
	#counts = collections.UserDict(counts)
	for k in counts.keys():
		counts[k] *= 1.0/s
		counts[k] = '%.4f'%(counts[k])
	return (counts)

# Returns a dictionary with the proportions of different types of speech
# This uses more complex tags like foreign words ('FW') and interjection ('UH')
# See this link for full list of tags --> http://www.nltk.org/book_1ed/ch05.html
def POSDensity(array):
	tagged = nltk.pos_tag(array);
	s = len(array)
	print(s)
	counts = dict( Counter(tag for word, tag in tagged))
	#counts = collections.UserDict(counts)
	for k in counts.keys():
		counts[k] *= 1.0/s
		counts[k] = '%.4f'%(counts[k])
	return (counts)


# Returns array of the length of each sentence
punct = [',', ';', ':', "''", "``" , '-', '—', '(',')' , '...']
def sentenceLength(tokenizedText):
	lens = []
	senlen = 0
	i = 0
	while i < len(tokenizedText):
		if tokenizedText[i] == ".":
			lens.append(senlen)
			senlen = 0
		elif tokenizedText[i] == "?" or tokenizedText[i]== "!":
			while i< len(tokenizedText)-1 and (tokenizedText[i+1] == "?" or tokenizedText[i+1]== "!"):
				i+=1
			lens.append(senlen)
			senlen = 0
		elif tokenizedText[i] not in punct:
			senlen = senlen + 1
		i+=1
	return lens

def senlenStats(text):
	senlen = sentenceLength(text)
	arr = []
	arr.append( statistics.mean(senlen) )
	#arr.append( statistics.median(senlen) )
	#arr.append( statistics.mode(senlen) )
	#arr.append( statistics.stdev(senlen) )
	return arr

# Returns the percent of a given text that is within quotes
def percentQuotes(array):
    count = 0
    length = len(array)
    for i in range(length):
        if array[i] == "``":
            i += 1
            while i < length and array[i] != "''":
                count += 1
                i += 1
            count += 2
    percent = count*1.0/length
    return percent

# Saves part of speech pi chart to graphs folder
def savePOSPiChart(text, title):
	ps = POSDensitySimple(text)
	labels = list(ps.keys())[0:5]
	sizes = list(ps.values())[0:5]

	rest = sum( float(x) for x in  list(ps.values())[5:])
	last = 'others'
	labels.append(last)
	sizes.append(rest)

	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'grey', 'brown']
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.title('Part of Speech Density')
	plt.savefig('templates/static/graphs/' + title + '.png')
	plt.close()



def saveSenLenHistogram(text, title):
	lens = sentenceLength(text)
	plt.plot(list(range(lens)), lens, 'ro')
	plt.show()

def findFreq (text, word):
    count = 0
    for w in text:
        if w == word:
            count+=1
    return count
    
def compareFreq (text, words):
    wordFreqs = []
    for word in words:
        wordFreqs.append(findFreq(text, word))
    print (wordFreqs)
    plt.bar(words, wordFreqs)
    plt.show()

#saveSenLenHistogram(cleanText('CatcherSalinger.txt'), 'cool.png')
#savePOSPiChart(cleanText('CatcherSalinger.txt'))

"""
text = nltk.Text(word.lower() for word in simpleTokenize("SoundAndFury.txt") )
print( text.similar('quentin') )
print( text.similar('benjy') )
print( text.similar('caddy') )
print( text.similar('jason') )
print( text.similar('dilsey') )
"""
#print( POSDensity ( cleanText("SoundAndFury.txt") ) )
