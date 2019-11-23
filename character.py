# coding=utf-8

# Character Study
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
import numpy as np
from simpleFunctions import simpleTokenize
from simpleFunctions import detokenize
from simpleFunctions import findFreq
from vector import vectorize2

# Randomly n text samples of word length l,
# of passage surrounding character char in given text

#sorry that this code is shit
def samplePassage(text, term, n, l):
	n = int(n)
	l = int(l)
	indices = []
	for i in range(len(text)):
		if text[i] ==  term:
			indices.append(i)
	if n>len(indices):
		n = len(indices)
	print (n)
	master = []
	while n > 0 and len(indices) > 0:
		x = indices[ random.randint(0, len(indices)-1 ) ]
		start  = int(x-l/2)
		while text[start-1] != '.' and text[start-1] != '?' and text[start-1] != '!' :
			start-= 1
		if start < 0:
			start = 0
		end = int(x+l/2)
		new = []
		i=0
		while i + start < len(text) and i + start < end:
			new.append(text[i + start])
			i+=1

		while i + start < len(text) and text[i+start] != '.' and text[i+ start] != '?' and text[i+ start] != '!':
			new.append(text[i + start])
			i+=1
		new.append('.')
		master.append(new)
		n = n-1
		indices.remove( x )

	for i in range(len(master)): 		#detokenize() adds '\' before some quotes, taking them out manually
		passage=detokenize(master[i])
		master[i]=passage
		if master[i][0] == "\\":
			master[i] = master[i][1::]
	return master

#sampledPassages = samplePassage(simpleTokenize('CatcherSalinger.txt'), "Spencer", 10, 50)

#print (detokenize(simpleTokenize('CatcherSalinger.txt')))
#for passage in sampledPassages:
#	print (passage)
#	print ("\n")
# Given an array of character names, does comparative analysis on the surrounding
# text of the characters
def characterCompare(text, chars):
	x = []
	for i in range(len(chars)):
		# 5 samples from each character
		sample = sampleCharacter(text, chars[i], 5, 200)
		temp = []
		# Creating vectors for each sample
		for j in range( len( sample )):
			temp.append( vectorize2(sample[j], ['retard', 'female', 'greedy', 'suicidal', 'incestuous'] ) )
		# Averaging sampled vectors
		x.append( np.mean(temp, axis=0).tolist() )
		#x.append(temp)
	print(x)

#characterCompare( simpleTokenize('SoundAndFury.txt'), ['Caddy', 'Benjy', 'Quentin', 'Jason', 'Dilsey'])
#print( np.mean([[3,5,7], [1,5,7], [3,6,7]], axis = 0).tolist() )
