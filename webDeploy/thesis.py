# Looking at theses, storing, better understanding

# How can you quantify/vectorize a thesis?
	# How much is bounded by --> , –– : ;
	# What are the verbs in the sentence? Which is the main verb?
	# What nouns are in the sentence? Which is the main noun?
	# Length of the clauses
	# therefore, however, nevertheless
	# listing ideas
# Other info
	# Topic sentences
	# Characters discussed
# Vector Components:
	# Proportion of nouns that are essential
	# Proportion of verbs that are essential
	# Proportion of bounded structures (within prepositions or commas or quotes)
	# Proportion of nouns that are pronouns

	# conjunction popularity (survey)

# future desires
	# train a chunker for Pingry student theses

import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import collections
from collections import Counter
from nltk.corpus import conll2000

POWERCONJUCTIONS = ['therefore', 'while', 'although', 'because', 'nevertheless', 'wherein', 'since', 'thereby', 'hence', 'thence']
BOUNDS = [',', '"', "––", " - ", ":", ";"]

# INPUT: thesis is assumed to be string input
def thesisVector(thesis, essentialNouns, essentialVerbs):
	words = nltk.word_tokenize(thesis)
	x = nltk.pos_tag(words)
	chunk =  nltk.ne_chunk(x)
	verbs = [ verb[0] for verb in x if verb[1][:2] == 'VB']
	nouns = [ noun[0] for noun in x if noun[1][:2] == 'NN']
	pronouns = [ p[0] for p in x if p[1] == 'PRON']
	pNoun = len(essentialNouns)*100.0/len(nouns)
	pVerb = len(essentialVerbs)*100.0/len(nouns)
	pPronoun = len(pronouns)*100.0/len(nouns)
	return { "Proportion of nouns you deemed essential" : "%.2f" % pNoun, "Proportion of verbs you deemed essential" : "%.2f" %pVerb, "Proportion of sentence bounded by punctuation (, –– ... etc.)" : "%.2f" %pBound(words), "Proportion of nouns that are pronouns": "%.2f" %pPronoun}

def pBound(words):
	stack = []
	x = 0
	for i in range(len(words)):
		if words[i] in BOUNDS:
			if not stack: # stack is empty
				stack.insert(0, words[i])
			else:
				stack.pop(0)
		if not not stack:
			x = x + 1
	return x*100.0/len(words)



m = thesisVector("The Muslim poets introduce Balram to the concept of jihad and thereby guide him toward a practical reconciliation between his inner conflicts and his more large-scale desires for reform, in such a way that combines the mechanisms of spitting and Murder Weekly. ", ['Balram', 'Murder', 'Weekly'], ['introduces'])
