import nltk
file = open("SoundAndFury.txt", "r")
words = nltk.word_tokenize(file.read())
print(words)

fdist = nltk.FreqDist(words)
print(fdist)

import matplotlib.pyplot as plt
fdist.plot(30,cumulative=False)
plt.show()