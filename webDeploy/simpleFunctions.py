import os

"""
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
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
from nltk.tokenize.treebank import TreebankWordDetokenizer
import statistics
import matplotlib.pyplot as plt, mpld3
import numpy as np
from nltk.corpus import stopwords

def getWordFreqDict(numWords):
	wordFreqDict = {}
	file = open("wordFreq.txt", "r")
	s = file.readline()
	while s != '' and numWords > 0:
		arr = []
		arr = s.split()
		wordFreqDict[arr[1]] = int(arr[2])
		wordFreqDict[arr[1]+'s'] = int(arr[2])
		wordFreqDict[arr[1]+'es'] = int(arr[2])
		s = file.readline()
		numWords = numWords - 1
	return wordFreqDict

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
	wfDict = getWordFreqDict(500)#ignore the most common 500 words: never display them
	counts = Counter(text)
	for w in counts.keys():
		if w.lower() in wfDict:
			counts[w] = 0
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
	plt.tight_layout()
	#fig = plt.figure()
	#if os.path.isfile('templates/static/graphs/' + title + '.png'):
	#	print("asdufb3oewj")
	#	os.remove('templates/static/graphs/' + title + '.png')
	plt.savefig('templates/static/graphs/' + title + '.png')
	plt.close()
	#return fig








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
	counts = dict( Counter(tag for word, tag in tagged))
	#counts = collections.UserDict(counts)
	for k in counts.keys():
		counts[k] *= 1.0/s
		counts[k] = '%.4f'%(counts[k])
	return (counts)

# Returns array of the length of each sentence
def sentenceLength(array):
	lens = []
	senlen = 0
	for word in array:
		if word == ".":
			lens.append(senlen)
			senlen = 0
		else:
			senlen = senlen + 1
	return lens

def senlenStats(text):
	senlen = sentenceLength(text)
	#arr = []
	#arr.append( statistics.mean(senlen) )
	#arr.append( statistics.median(senlen) )
	#arr.append( statistics.mode(senlen) )
	#arr.append( statistics.stdev(senlen) )
	return statistics.mean(senlen)

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
	#plt.title('Part of Speech Density')
	plt.tight_layout()
	plt.savefig('templates/static/graphs/' + title + '.png')
	plt.close()
#text = cleanText("CatcherSalinger.txt")
#print (savePOSPiChart(text, "test"))



def saveSenLenHistogram(text, title):
	lens = sentenceLength(text)
	plt.plot(list(range(lens)), lens, 'ro')
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
