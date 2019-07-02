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
from test import simpleTokenize
from vector import vectorize2

# Randomly n text samples of word length l, 
# of passage surrounding character char in given text
def sampleCharacter(text, char, n, l):
	indices = []
	for i in range(len(text)):
		if text[i] ==  char:
			indices.append(i)
	master = []
	while n > 0 and len(indices) > 0:
		x = indices[ random.randint(0, len(indices)-1 ) ]
		start  = int(x-l/2)
		if start < 0:
			start = 0
		new = []
		for i in range(l):
			if i + start < len(text):
				new.append(text[i + start])
		master.append(new)
		n = n-1
		indices.remove( x )
	return master
		
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
	
characterCompare( simpleTokenize('SoundAndFury.txt'), ['Caddy', 'Benjy', 'Quentin', 'Jason', 'Dilsey'])
#print( np.mean([[3,5,7], [1,5,7], [3,6,7]], axis = 0).tolist() )
