import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys
from test import simpleTokenize
import wikipedia
import statistics
from scipy import stats
from nltk.tokenize.treebank import TreebankWordDetokenizer
import matplotlib.pyplot as plt
import random


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

# Generates a list of a list of related words, based on wikipedia page
# for the given list
# Given ogWords=[yellow, fish] and numWords = 2
# [[color, orange], [gill-bearing, aquatic]]
def wikipediaWords(ogWords, numWords):
	list = []
	for i in range(len(ogWords)):
		try:
			text = nltk.Text(cleanText(nltk.word_tokenize(wikipedia.page(title = ogWords[i]).summary)))
			list.append(text[1:numWords])
		except wikipedia.exceptions.DisambiguationError as e:
			print(ogWords[i] + " caused disambiguation error")
			list.append([])
	return list

# Default finder of first generation words
# Randomly samples
def firstgen(fileName):
	w = cleanText( simpleTokenize(fileName) )
	w = set(w)
	lim = 5 + random.randint(0,3)
	w = [o for o in w if len(o) >= lim]
	ret = []
	for i in range(30):
		rand = random.randint(0, len(w)-1)
		ret.append( w[rand] )
		w.pop(rand)
	return ret

# Generates an second generation of words, based on the context in rootTextNae
# and a given array of first gen words picked out by human reading.
def nextGeneration(rootTextName, newDocName, words):
	text = nltk.Text(word.lower() for word in simpleTokenize(rootTextName) )
	sys.stdout = open(newDocName, 'w')
	for i in range(len(words)):
		# Original word
		print(words[i])
		# Context words within document
		text.similar(words[i], 1)
		# Context words from Wikipedia
		w = wikipediaWords(words, 7)
		for j in range(len(w[i])):
			print(w[i][j])
	sys.stdout = sys.__stdout__
	m = simpleTokenize(newDocName)
	n = m.copy()
	for i in range(len(m)):
		if m[i] == "No" and m[i+1] == "matches":
			n.remove("No")
			n.remove("matches")
	return n

#print nextGeneration("CatcherSalinger.txt", "eskimoWords.txt", ['yes'])

# Word Progression Report
# Giving stats and info from the word progression, specifically the 100 word block
# with the highest score
def wpReport(filename, firstgen, secgen, ssName, numTop):
	str = ""
	str = "\n\n\nTitle: " + ssName + "\n"
	str += "FirstGen Words: " + str(firstgen)+ "\n"
	str += "SecondGen Words: " + str(secgen) + "\n"
	text = simpleTokenize(filename)
	arr = wordProgression(text, firstgen, secgen)
	for i in range(numTop):
		topIndex = arr.index(max(arr))
		topWords = text[topIndex*100:topIndex*100+100]
		str+="\n\nNumber " + str(i) + "\n"
		str+= "--> Score: " + str( arr[topIndex]) + "\n--> Z-Score: " + str(stats.zscore(arr)[topIndex]) + "\n"
		str+="--> Average Score " + str(statistics.mean(arr)) + "\n"
		fg=0
		sg=0
		for i in range(len(topWords)):
			if topWords[i] in firstgen:
				fg+=1
			if topWords[i] in secgen:
				sg+=1
		str+="Number of FirstGen Words: " + str(fg) + "\n"
		str+="Number of SecondGen Words: " + str(sg) + "\n"
		str+= TreebankWordDetokenizer().detokenize(topWords) + "\n"
		del arr[arr.index(max(arr))]
	return str

def plotChronoMap(textName, firstgen, secgen, title):
	#fig, axs = plt.subplots(1)
	#fig.suptitle('Short Story Readings on Salinger')
	t = nltk.Text(word.lower() for word in simpleTokenize(textName))
	y = wordProgression( t , firstgen, secgen)
	x =  list(range( int(len(t)/100) +1))
		# If you want to make separate plots
	plt.plot(x,y)
	plt.savefig('/templates/static/graphs/' + title + '.png')
	#axs[graphNum].plot(x, y)
	#axs[graphNum].set_title(title)
	#wpReport(writeTo, firstgen, secgen, title, 3, writeTo)

def wordProgression(text, firstgen, secgen):
    occurences = []
    section = list(range(100))
    ocount = 0
    i = 0
    while i < len(text):
        j = i
        while i < j + 100 and i < len(text):
            if text[i] in firstgen:
                ocount += 4
            elif text[i] in secgen:
            	ocount += 1
            i += 1
        occurences.append(ocount)
        ocount = 0
    return occurences

# Given a filename, returns an array of tokens (words, punctuation are separated)
def simpleTokenize(fileName):
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	return words


# Master algorithm
# Takes in
	# baseText (name of text being mapped out in terms of its similarities to the metricText)
	# metricText (name of text where we generate levels of words and apply to baseText)
	# firstgen (array of read words)
	# writeTo (filename destination for report)
# Result:
	# Document containing key passages and statistics regarding the words found
	# Graph showing the chronological readings of the metricText along the baseText
def master(baseText, metricText, firstgen, writeTo):
	#simpleTokenize(metricText)
	simpleTokenize(baseText)
	secgen = nextGeneration(baseText, writeTo, firstgen)
	wpReport(baseText, firstgen, secgen, metricText, 5)
	plotChronoMap(baseText, firstgen, secgen, metricText)

bw = ['yellow', 'fish', 'glass', 'foot', 'beach', 'suicide']
#master("CatcherSalinger.txt", "Bananafish", bw, "bananaWords.txt")

tw = ['teddy', 'poet', 'gift horse', 'nephritis', 'diary', 'orphan', 'triumvirate', 'myriad' ] # cut spiritual
#master("CatcherSalinger.txt", "Teddy", tw, "teddyWords.txt")

lw = ['chief','museum', 'baseball', 'laugh', 'descendant']
#master("CatcherSalinger.txt", "Laughing Man", lw, "laughingWords.txt")

ew = ['esme', 'love', 'squalor', 'wedding', 'faculties', 'war']
#master("CatcherSalinger.txt", "Esme", ew, "esmeWords.txt")

#plt.show()
