import nltk
import random
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys
import copy
import requests

# Given a filename, returns an array of tokens (words, punctuation are separated)
def simpleTokenize(fileName):
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	return words

# This function should, given a fileName, 1) tokenize the text file
# 2) remove three or fewer characters, 3) Removing stopwords
# 4) Lemmatization (third person-->first person, past to present tense)
# 5) Stemming (root form of word)
# Return the tokenized array
def cleanText(fileName,allLower):
	lem = WordNetLemmatizer()
	stem = PorterStemmer()
	file = open(fileName, "r")
	words = nltk.word_tokenize(file.read())
	stop_words=set(stopwords.words("english"))
	filteredDict = []
	for w in words:
		if w not in stop_words and len(w)>3:
			w = lem.lemmatize(w,"v")
			filteredDict.append(w.lower())
	return filteredDict

def getWordFreqDict():
    wordFreqDict = {}
    file = open("wordFreq.txt", "r")
    s = file.readline()
    while s != '':
        arr = []
        arr = s.split()
        if len(arr) != 3:
            print(arr[1])
        wordFreqDict[arr[1]] = int(arr[2])
        wordFreqDict[arr[1]+'s'] = int(arr[2])
        wordFreqDict[arr[1]+'es'] = int(arr[2])
        s = file.readline()
    return wordFreqDict

def compare(d1, d2,wordFreq):#compares two texts given their dictionaries of words and returns overlaping words
    d = {}
    abcd = 0
    for w in d1.keys():
        if w in d2:
            #if w in wordFreq:
            #    d[w] = min(d1[w],d2[w]) / wordFreq[w] # min(d1[w],d2[w]) is number of references, but we want to scale this based on the word's general word frequency
            #else:
            #    d[w] = min(d1[w],d2[w]) / 1
            if min(d1[w],d2[w]) < 4 or w == "could":
                continue
            response = requests.get("https://api.datamuse.com/words?sp=" + w + "&md=f&max=1")
            if len(response.json()) != 0:
                wf = str(response.json()[0]["tags"][0])
                wf = float(wf[2:len(wf)])
                if wf < 0.1:
                    wf = 0.1
                if wf > 50:
                    continue
                d[w] = min(d1[w],d2[w]) / wf
                abcd += 1
                print(abcd)
    return d

def overlap(texts, n):#compares n texts at a time; returns overlapDict where overlapDict[0][i] has the texts compared, and overlapDict[1][i] is a list of tuples where the first element is the word sorted based on relative frequencies, and the second element is the relative frequency
    wordFreq = getWordFreqDict()
    wordDicts = []#one for each text
    for i in range(len(texts)):
        newDict = {}
        for j in range(len(texts[i])):
            if texts[i][j] in newDict:
                newDict[texts[i][j]] += 1
            else:
                newDict[texts[i][j]] = 1
        wordDicts.append(newDict)
    #overlapHelper(texts, wordDicts, allCompare,0)
    textIdx = []
    currTextIdx = n - 1 #text whose index needs to be itterated
    overlapDict = []#first element holds indices of texts being compared, second element holds the overlap
    overlapDict.append([])
    overlapDict.append([])
    for i in range(n):
        textIdx.append(i)
    while 1:
        currOverlap = wordDicts[textIdx[0]]
        for i in range(1,n):
            currOverlap = compare(currOverlap, wordDicts[textIdx[i]],wordFreq)
        overlapDict[0].append(textIdx.copy())
        overlapDict[1].append(sorted(currOverlap.items(), key = lambda kv:(-kv[1], kv[0])))
        if textIdx[currTextIdx] == currTextIdx - n + len(texts):
            currTextIdx -= 1
            if currTextIdx == -1:
                break
            if textIdx[currTextIdx] == currTextIdx - n + len(texts):#case where n = len(texts)
                break
        textIdx[currTextIdx] += 1
    return overlapDict



#parameters = {"lat": 40.71, "lon": -74}
"""w = "nine-thirty"
response = requests.get("https://api.datamuse.com/words?sp=" + w + "&md=f&max=1")
print(response.json())
print(response.json()[0]["tags"][0])
wf = str(response.json()[0]["tags"][0])
wf = wf[2:len(wf)]
print(wf)"""

getWordFreqDict()
numDocs = 2
texts = []
#for i in range(numDocs):
#    fileName = "D" + str((i+3)) + ".txt";
#    texts.append(cleanText(fileName,1))
texts.append(cleanText("AILDFaulkner.txt",1))

texts.append(cleanText("CatcherSalinger.txt",1))
result = overlap(texts,2)
for i in range(len(result[0])):
    print("texts:")
    for j in range(len(result[0][i])):
        print(result[0][i][j])
    print("associated words:")
    for j in range(50):#len(result[1][i])):
        print(str(result[1][i][j][0]))
