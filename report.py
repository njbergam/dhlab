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
from nltk.tokenize.treebank import TreebankWordDetokenizer



# Word Progression Report
# Giving stats the info in WordProg, specifically the 100 words with the highest score
def wpReport(filename, firstgen, secgen, ssName, numTop, writeTo):
	sys.stdout = open(writeTo, 'w')
	print("FirstGen Words: " + str(firstgen))
	print("SecondGen Words: " + str(secgen))
	text = simpleTokenize(filename)
	arr = wordProgression(text, firstgen, secgen)
	print( "\n\n\nTitle: " + ssName )
	for i in range(numTop):
		topIndex = arr.index(max(arr))
		topWords = text[topIndex*100:topIndex*100+100]
		print("\n\nNumber " + str(i))
		print( "--> Score: " + str( arr[topIndex]) + "\n--> Z-Score: " + str(stats.zscore(arr)[topIndex]))
		print("--> Average Score " + str(statistics.mean(arr))) 
		fg=0
		sg=0
		for i in range(len(topWords)):
			if topWords[i] in firstgen:
				fg+=1
			if topWords[i] in secgen:
				sg+=1
		print("Number of FirstGen Words: " + str(fg))
		print("Number of SecondGen Words: " + str(sg))
		print( TreebankWordDetokenizer().detokenize(topWords))
		del arr[arr.index(max(arr))]
	sys.stdout = sys.__stdout__
	
	

# Banana Fish
bw = ['yellow', 'fish', 'glass', 'foot', 'beach', 'suicide']
bwArray = generateSimilarWords("CatcherSalinger.txt", "bananaWords.txt", bw) 

# Teddy 
tw = ['teddy', 'poet', 'gift horse', 'nephritis', 'spritual', 'diary', 'orphan', 'triumvirate', 'myriad' ]
twArray = generateSimilarWords("CatcherSalinger.txt", "teddyWords.txt", tw)

# The Laughing Man
lw = ['chief','museum', 'baseball', 'laugh', 'descendant']
lwArray = generateSimilarWords("CatcherSalinger.txt", "laughingWords.txt", lw)

# For Esme – With Love and Squalor
ew = ['esme', 'love', 'squalor', 'wedding', 'faculties', 'war']
ewArray = generateSimilarWords("CatcherSalinger.txt", "esmeWords.txt", ew)

# Daumier-Smith
dw = ['el greco', 'french', 'tokyo', 'art', 'buddhism', 'lying',  'harvard', 'nun', 'magdalene']
dwArray = generateSimilarWords("CatcherSalinger.txt", "daumierWords.txt", dw)
	
wpReport("CatcherSalinger.txt", bw, bwArray, "A Perfect Day for Bananafish", 3, "bananaWords.txt") 
wpReport("CatcherSalinger.txt", lw, lwArray, "The Laughing Man", 3, "laughingWords.txt") 
wpReport("CatcherSalinger.txt", ew, ewArray, "For Esme––With Love and Squalor", 2, "esmeWords.txt") 
wpReport("CatcherSalinger.txt", tw, twArray, "Teddy", 1, "teddyWords.txt") 
wpReport("CatcherSalinger.txt", dw, dwArray, "Daumier-Smith", 1, "daumierWords.txt") 


