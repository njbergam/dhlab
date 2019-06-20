import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
import sys
from test import simpleTokenize
from visuals import wordProgression
from visuals import generateSimilarWords
import statistics
from scipy import stats

# Word Progression Report
# Giving stats the info in WordProg, specifically the 100 words with the highest score
def wpReport(filename, firstgen, secgen, ssName):
	text = simpleTokenize(filename)
	arr = wordProgression(text, firstgen, secgen)
	topIndex = arr.index(max(arr))
	topWords = text[topIndex*100:topIndex*100+100]
	print( ssName )
	print( "Top 100 Words --> Score: " + str( arr[topIndex]) + ", --> Z-Score: " + str(stats.zscore(arr)[topIndex]))
	print("Average Score --> " + str(statistics.mean(arr))) 
	#print("Number of FirstGen Words: " + )
	#print("Number of SecondGen Words: " + )
	print(topWords)
	
	
	
ew = ['esme', 'love', 'squalor', 'wedding', 'faculties', 'war']
ewArray = generateSimilarWords("CatcherSalinger.txt", "esmeWords.txt", ew)
	
wpReport("CatcherSalinger.txt", ew, ewArray, "For Esme––With Love and Squalor") 