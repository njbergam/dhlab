import nltk
import random
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys

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


def LDA(texts,K):
    #initialization
    topicLst = []#topicLst[topic][word] returns how many times that word occurs in that topic, wordsByTopic
    topicLength = []
    for i in range(K):
        newDict = {}
        topicLst.append(newDict)
        topicLength.append(0)
    wordToGroup = [] #the indices here correspond to texts: texts[i][j] corresponds to group wordToGroup[i][j]
    for i in range(len(texts)):
        newLst = []
        wordToGroup.append(newLst)
    for i in range(len(texts)):
        for j in range(len(texts[i])):
            assignment = random.randint(0,K - 1)#the topic that the word will be assigned to
            topicLength[assignment] += 1
            #update wordList
            wordToGroup[i].append(assignment)
            #update topicLst
            if texts[i][j] in topicLst[assignment]:
                topicLst[assignment][texts[i][j]] += 1
            else:
                topicLst[assignment][texts[i][j]] = 1
    for a in range(10):#arbitrary number of iterations for now
        for i in range(len(texts)):
            wordsPerTopic = []
            for k in range(K):
                wordsPerTopic.append(0)
            for j in range(len(texts[i])):
                wordsPerTopic[wordToGroup[i][j]] += 1
            for j in range(len(texts[i])):
                #calculate assignment probabilities to each topic: all assignmentProbabilities should add to 1
                assignmentProbabilities = []
                sumProbabilities = 0
                for topic in range(K):
                    #calculate proportion of words in document d that are assigned to topic t
                    p1 = wordsPerTopic[topic] / len(texts[i]);
                    #proportion of assignments to topic t, over all documents d, that come from word w
                    p2 = 0
                    if texts[i][j] in topicLst[topic]:
                        p2 = topicLst[topic][texts[i][j]]
                    p2 /= topicLength[topic]
                    assignmentProbabilities.append(p1*p2)
                    sumProbabilities += p1*p2
                #choose new topic
                rand = random.uniform(0,sumProbabilities)
                chosenTopic = 0
                rand -= assignmentProbabilities[0]
                while rand > 0 and chosenTopic < K - 1:
                    chosenTopic += 1
                    rand -= assignmentProbabilities[chosenTopic]
                #reassign topic
                """if wordToGroup[i][j] == chosenTopic:
                    print("not switch")
                else:
                    print("switch")"""
                wordsPerTopic[wordToGroup[i][j]] -= 1
                wordsPerTopic[chosenTopic] += 1
                topicLength[wordToGroup[i][j]] -= 1
                topicLength[chosenTopic] += 1
                topicLst[wordToGroup[i][j]][texts[i][j]] -= 1
                if texts[i][j] in topicLst[chosenTopic]:
                    topicLst[chosenTopic][texts[i][j]] += 1
                else:
                    topicLst[chosenTopic][texts[i][j]] = 1
                wordToGroup[i][j] = chosenTopic
    #format return: proportion of words in document d that are assigned to each topic t is proportions[d][t]
    wordsPerTopicByText = []
    for i in range(len(texts)):
        wordsPerTopic = []
        for k in range(K):
            wordsPerTopic.append(0)
        for j in range(len(texts[i])):
            wordsPerTopic[wordToGroup[i][j]] += 1
        wordsPerTopicByText.append(wordsPerTopic)
    #topicWords = []
    #for topic in range(K):
    #    topicWords.append(topicLst[topic].keys())
    ret = []
    ret.append(wordsPerTopicByText)
    ret.append(topicLst)
    return ret


numDocs = 5
texts = []
for i in range(numDocs):
    fileName = "D" + str((i+1)) + ".txt";
    texts.append(cleanText(fileName))
numCategories = 4
result = LDA(texts,numCategories)
documentTopicDistribution = result[0]
for i in range(numDocs):
    print("----------document " + str(i) + "------------")
    for topic in range(numCategories):
        print(documentTopicDistribution[i][topic])
wordsByTopic = result[1]
for topic in range(numCategories):
    print("----------topic " + str(topic) + "------------")
    wordsInTopic = wordsByTopic[topic].keys()
    for word in wordsInTopic:
        if wordsByTopic[topic][word] > 2:
            print(str(word) + ":" + str(wordsByTopic[topic][word]))
