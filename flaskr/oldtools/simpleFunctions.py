# Noah: We should find a way to make sure all these graph making functions are saving to the right place

import os
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
from PyPDF2 import PdfFileReader

def extract_entity_names(t):#pulled from https://www.mapping-tools.com/howto/maptitude/programming-topics/using-python3-to-draw-annotation/
	entity_names = []
	if hasattr(t, 'label') and t.label:
		if t.label() == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))
	return entity_names

def getNames(in_file):#too slow
	main_text = ""
	with open(in_file, 'r') as f:
		for line in f:
			main_text = main_text + line
	sentences = nltk.sent_tokenize(main_text)
	i = 0
	k = len(sentences)
	for j in range(1,k):#speed up: only look at every 5th sentence
		i += 1
		if i % 10 != 0:
			del sentences[k-j]
	# Tokenize the sentences - ie. split them into words
	tokenized_sents = [nltk.word_tokenize(sentence) for sentence in sentences]
	# Tag these words with Part-of-Speech tags (noun, verb, etc)
	tagged_sents = [nltk.pos_tag(sentence) for sentence in tokenized_sents]
	# Create named entity chunks from these tagged words
	chunked_sents = nltk.ne_chunk_sents(tagged_sents, binary=True)
	# Extract a list of named entities (people, places, etc)
	entities = []
	for tree in chunked_sents:
		entities.extend(extract_entity_names(tree))
	print(entities)

def removeProperNouns(text):
	maxLen = len(text)
	for i in range(1,maxLen+1):
		if text[maxLen - i][0].isupper():
			del text[maxLen - i]
	return text

def text_extractor(pdfFile):
	with open(pdfFile, 'rb') as f:
		pdf = PdfFileReader(pdfFile)
		text = ""
		for i in range(pdf.getNumPages()):
			page = pdf.getPage(i)
			text += page.extractText()
	return nltk.word_tokenize(text)

# Returns the frequency of a given word in a text
def findFreq (text, word):
    count = 0
    for w in text:
        if w == word:
            count+=1
    return count

# Creates a bar graph showing different freuqencies of different words within a given text (text in list form)
def compareFreq (text, words):
    wordFreqs = []
    for word in words:
        wordFreqs.append(findFreq(text, word))
    print (wordFreqs)
    plt.bar(words, wordFreqs)
    plt.show()

def txtToLower (text):
	lowerText = []
	for i in range(len(text)):
		lowerText.append(text[i].lower())
	return lowerText


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

# This function should, given a fileName, 1) tokenize the text file
# 2) remove three or fewer characters, 3) Removing stopwords
# 4) Lemmatization (third person-->first person, past to present tense)
# 5) Stemming (root form of word)
# Return the tokenized array
def cleanText2(words):
	lem = WordNetLemmatizer()
	#s = PorterStemmer()
	stop_words=set(stopwords.words("english"))
	filteredDict = []
	for w in words:
		if w not in stop_words and len(w)>3:
			w = lem.lemmatize(w,"v")
			#w = s.stem(w)
			filteredDict.append(w)
	return filteredDict

# Tokenizes a comma-delimited string into a list
def deList(str):
	str = str.replace(" ", "")
	return str.split(",")

# Given a filename, returns an array of tokens (words, punctuation are separated)
def simpleTokenize(fileName):
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	return words

# Given a piece of text as a list, detokenizes and returns it back into a string
def detokenize(text):
	return TreebankWordDetokenizer().detokenize(text)

# Creates and saves a bar graph of the most common words in a text
def saveTopWords(text, title):
	text = removeProperNouns(text)
	text = txtToLower(text)
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

def POSColor(thesis):
	words = nltk.word_tokenize(str(thesis))
	tagged = nltk.pos_tag(words)
	simplifiedTags = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in tagged]
	print(simplifiedTags)
	colorTags = []
	for i in range(len(simplifiedTags)):
		word = []
		word.append(simplifiedTags[i][0])
		if simplifiedTags[i][1] == 'NOUN':
			word.append('006600')
		elif simplifiedTags[i][1] == 'ADJ':
			word.append('0000FF')
		elif simplifiedTags[i][1] == 'VERB':
			word.append('990099')
		elif simplifiedTags[i][1] == 'PRON':
			word.append('FF8000')
		elif simplifiedTags[i][1] == 'ADV':
			word.append('CC0000')
		else:
			word.append('000000')
		colorTags.append(word)
	return colorTags


# Returns a dictionary with the proportions of different types of speech
# This uses simplified tags, so it only contains nouns, verbs, adjectives, pronouns, and adverbs
def POSDensitySimple(array):
	tagged = nltk.pos_tag(array)
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
	tagged = nltk.pos_tag(array)
	s = len(array)
	counts = dict( Counter(tag for word, tag in tagged))
	#counts = collections.UserDict(counts)
	for k in counts.keys():
		counts[k] *= 1.0/s
		counts[k] = '%.4f'%(counts[k])
	return (counts)

# Returns array of the length of each sentence
def sentenceLength(tokenizedText):
	punct = [',', ';', ':', "''", "``" , '-', '—', '(',')' , '...']
	lens = []
	senlen = 0
	i = 0
	while i < len(tokenizedText):
		if tokenizedText[i] == ".":
			prevI = i
			while i< len(tokenizedText)-1 and tokenizedText[i+1] == ".":#ellipses
				i+=1
			if prevI == i:
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

# Returns an array of different one-variable parameters regarding sentence length
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


# Shows a histogram of sentence lengths
# STILL NEEDS TO SAVE THEM
def saveSenLenHistogram(text, title):
	lens = sentenceLength(text)
	plt.plot(list(range(lens)), lens, 'ro')
	plt.show()
