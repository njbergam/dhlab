# AmericanModernism (N. Bergam, J. Li)
We are the digital humanities pioneers for the Pingry School's Humanities Independent Research Team. We are currently in the process of investigating two topics.

## Mission 1: The "Infinity Stones" of Salinger's Short Stories

We believe there are some convincing thematic and character similarities between the 'Nine Stories' and the various 'episodes' of Holden's journey in 'The Catcher in the Rye.' These are specific comparisons we have in mind, from our own reading. 
     1. Mr. Antonelli and Seymour Glass: Why is Salinger pressuring the reader to assume these men are pedophiles?
     2. Holden and Teddy: Advanced Wisdom or Fatal Naivete?
     3. Buddhism and the Void in American Culture: Caulfield vs de-Daumier Smith
     4. PTSD: Addressed directly for 'Esme', perhaps indirectly for 'Catcher'
     5. The Death of Youthful Constructs: 'Laughing Man' and the 'Rye' poem
     
Through digital humanities techniques like Topic Modeling, we can illuminate these connections qualitatively and furthermore establish new connections.

Our experimental design is as follows:
1. Generate key words and phrases from individual short stories through human reading (e.g. “glass” or “fish” from “A Perfect Day For Bananafish“)
2. Generate a second generation of similar words from this initial human reading list
    1. Currently, we are using nltk’s text.similar(), which uses word context and part of speech to generate list of words
    2. However, we are hoping we can use more advanced machine learning designs (taking information and context from other texts) to generate better second generation batch
3. Using the frequency of these words across Catcher in the Rye (as well as some sort of weighting system between first and second gen words, as well as within generations) to produce a heat map of the word frequencies of keywords for each short story in relation to Catcher
4. Using human reading, divide Catcher in the Rye into certain chapters and mark this on the heat map (e.g. “first taxi driver”, “Mr. Antonelli”, “fight with Stradlater”)
5. Use these heat maps to confirm hypotheses / find new connections. Conduct further tests to measure similarity in writing style (sentence length, word strength, etc.)

## Mission 2: Themes in Children's Storytelling

## Future

Up to this point, we have treated texts as a “bag of words”; we’ve split up novels into arrays of singular words and focused on the frequency and similarity of individual words rather than how these words might interact with each other. Although it has allowed us to write a variety useful functions, our current method of analysis is constrained by its superficiality.  By creating algorithms which examine larger word combinations and the interplay between words and phrases,  we may be able to gain  more “human” understandings of texts and ultimately draw more accurate meaningful observations.
