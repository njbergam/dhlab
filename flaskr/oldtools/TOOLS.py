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
	s = PorterStemmer()
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

# Given a filename, returns an array of tokens (words and punctuation are separated)
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
	plt.savefig('../static/graphs/' + title + '.png')
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
    percent = (count*1.0 -0.01)/(length-0.01)
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
	plt.savefig('../static/graphs/' + title + '.png')
	plt.close()
#text = cleanText("CatcherSalinger.txt")
#print (savePOSPiChart(text, "test"))


# Shows a histogram of sentence lengths
# STILL NEEDS TO SAVE THEM
def saveSenLenHistogram(text, title):
	lens = sentenceLength(text)
	plt.plot(list(range(lens)), lens, 'ro')
	plt.show()


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


def syllable_count(word):
    word=word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count


def flesch_read(str):
    """
    RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)
    Gives 0-100, where 0-30 is college grad level and 100-90 is 5th grade
    """
    words = nltk.word_tokenize(str)
    ASL = statistics.mean( sentenceLength(words) )
    ASW = statistics.mean( [syllable_count(word) for word in words] )
    return round( 206.835-(1.015 * ASL)-(84.6 * ASW) , 3)

def flesch_kincaid_read(str):
    """
    RE = 0.39 * ASL + 11.8 * ASW - 15.59
    Gives a grade level (1-12)
    """
    words = nltk.word_tokenize(str)
    ASL = statistics.mean( sentenceLength(words) )
    ASW = statistics.mean( [syllable_count(word) for word in words] )
    return round( (0.39 * ASL) + (11.8 * ASW) - 15.59, 3)


def fog_read(str):
    """
    RE = 0.4 (ASL + PHW)
    PHW = percent hard words (3+ syllables, not proper, not compound/hyphen of easy words, verbs with added -es/-ed)
    Gives an approximate grade level (1-12)
    """
    words = nltk.word_tokenize(str)
    ASL = statistics.mean( sentenceLength(words) )
    PHW = phw(words)
    return round( 0.4 * (ASL + PHW),3)

def phw(words):
    """
    Gives the percentage of hard words in a given piece of text
    hard meaning --> (3+ syllables, not proper, not compound/hyphen of easy words, verbs with added -es/-ed)
    """
    count = 0
    for word in words:
        if syllable_count(word) >= 3 and nltk.pos_tag(word)[0][1] != 'NNP':
            count+=1
    return round(count*100.0/len(words),3)

# Randomly n text samples of word length l,
# of passage surrounding character char in given text

#sorry that this code is shit - justin li '2021
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

def tfidf(word, text, corpus):
    freq = 0
    N = len(corpus)
    for currword in text:
        if currword == word:
            freq += 1
    count = 0
    for currtext in corpus:
        for currword in currtext:
            if currword == word:
                count += 1
                break
    tf = math.log(1+freq)
    idf = math.log((N+2)/(count+1))
    return tf*idf
