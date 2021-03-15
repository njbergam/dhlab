import nltk
import statistics
from simpleFunctions import sentenceLength

"""
This script will house functions that give back certain readability indexes for texts
All _read functions are READABILITY algorithms
--> take in strings, that they then tokenize into lists themselves
"""

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
