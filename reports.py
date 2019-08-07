import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys
from simpleFunctions import *
import wikipedia
import statistics
from scipy import stats
from nltk.tokenize.treebank import TreebankWordDetokenizer
import matplotlib.pyplot as plt
import random

punct = ['.', ',', '\"', '?']

def wordProgressionWeighted(text, firstgen, secgen):
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

def wordProgression (text, words):
    occurences = []
    section = list(range(100))
    ocount = 0
    i = 0
    while i < len(text):
        j = i
        while i < j + 100 and i < len(text):
            if text[i] in words:
                ocount += 1
            i += 1
        occurences.append(ocount)
        ocount = 0
    return occurences



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


# Our (better) version of NLTK.similar()
# Goes through each word w, finds w1-w-w2
# Goes through text and looks for words also in that sandwich
# Returns firstgen words in list as well
def similarContext(text, firstgen):
    pairs = []
    similar = []
    # Getting the words directly ahead and behind
    for i in range(len(text)):
        if text[i] in firstgen and text[i-1] != '.' and text[i+1] != ',' and text[i-1] not in stopwords.words("english"):
            pairs.append( [text[i-1], text[i+1]] )

    firsts = [ pair[0] for pair in pairs]
    seconds = [ pair[1] for pair in pairs]
    for i in range(len(text)):
        if text[i] in firsts and text[i+2] in seconds:
            similar.append(text[i+1])
    return list(set(similar))

numWordsPerSection = 100

# Word Progression Report
# Giving stats and info from the word progression, specifically the 100 word blocks
# with the highest scores
def wpReport(text, firstgen, secgen, numTop):
    global numWordsPerSection
    list = []
    list.append( "FirstGen Words: " + str(firstgen)+ "\n")
    list.append( "DocumentContext Words: " + str(secgen) + "\n")
    list.append( "WikipediaContext Words" + str(wikipediaWords(firstgen, 3)) + "\n")
    arr = wordProgression(text, firstgen, secgen)
    for i in range(numTop):
        s = ''
        topIndex = arr.index(max(arr))
        topWords = text[topIndex*numWordsPerSection:topIndex*numWordsPerSection+numWordsPerSection]
        s+="\n\n\nNumber " + str(i) + "\n"
        s+= "--> Score: " + str( arr[topIndex]) + "\n--> Z-Score: " + str(stats.zscore(arr)[topIndex]) + "\n"
        s+="--> Average Score " + str(statistics.mean(arr)) + "\n"
        fg=0
        sg=0
        for i in range(len(topWords)):
            if topWords[i] in firstgen:
                fg+=1
            if topWords[i] in secgen:
                sg+=1
        s+="Number of FirstGen Words: " + str(fg) + "\n"
        s+="Number of SecondGen Words: " + str(sg) + "\n"
        s+= TreebankWordDetokenizer().detokenize(topWords) + "\n"
        del arr[arr.index(max(arr))]
        list.append(s)
    return list

def oneTextPlotChronoMap (text, wordlists, title):
    y = []
    x =  list(range( int(len(text)/numWordsPerSection) +1))
    for i in range(len(wordlists)):
        #print (i)
        y.append(wordProgression(txtToLower(text), wordlists[i]))
        #print (y)
        #plt.title("Word Group Progressions through Novel")
        plt.ylabel("Num occurances per 100 words")
        plt.xlabel("Progression of novel (by every 100 words)")
        lbl = str(wordlists[i][0])
        for j in range(1,len(wordlists[i])):
            lbl += ", " + str(wordlists[i][j])
        plt.bar(x, y[i], label = lbl)
        plt.legend()
    plt.savefig('templates/static/graphs/' + title + '.png')
    plt.close()

#text = cleanText("CatcherSalinger.txt")
#plotChronoMap(text, [["hate"], ["love"]],"test")

def saveChronoMap(text, firstgen, secgen, title):
    y = wordProgression( text , firstgen, secgen)
    x =  list(range( int(len(text)/numWordsPerSection) +1))
    plt.plot(x,y)
    plt.savefig('templates/static/graphs/' + title + '.png')
    plt.close()



# Randomly n text samples of word length l,
# of passage surrounding character char in given text
# Returns a dictionary where each piece is (startindex:passage)
def sampleCharacter(text, char, n, l):
	indices = []
	for i in range(len(text)):
		if text[i] ==  char:
			indices.append(i)
	master = {}
	while n > 0 and len(indices) > 0:
		x = indices[ random.randint(0, len(indices)-1 ) ]
		start  = int(x-l/2)
		if start < 0:
			start = 0
		new = []
		for i in range(l):
			if i + start < len(text):
				new.append(text[i + start])
		master.update( {start : TreebankWordDetokenizer().detokenize(new) } )
		n = n-1
		indices.remove( x )
	return master
