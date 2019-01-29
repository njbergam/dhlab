/**
The Flesch Reading Ease Readability Formula

The specific mathematical formula is:

RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)

RE = Readability Ease

ASL = Average Sentence Length (i.e., the number of words divided by the number of sentences)

ASW = Average number of syllables per word (i.e., the number of syllables divided by the number of words)

The output, i.e., RE is a number ranging from 0 to 100. The higher the number, the easier the text is to read.

• Scores between 90.0 and 100.0 are considered easily understandable by an average 5th grader.

• Scores between 60.0 and 70.0 are considered easily understood by 8th and 9th graders.

• Scores between 0.0 and 30.0 are considered easily understood by college graduates.
**/

public class HiRTAnalysis{

  public static void main(String[] args){

  }
}

class Text{
  private String filename;
  private String narrator;
  private WordFrequency wf;
  private SentenceStructure ss;



}

class WordFrequency{



  // keeps dictionary of all occurences of all words

  public int numOccurrences(String word){
    return 0;
  }

}

class SentenceStructure{
  //count numbers of types of sentences (complex, simple, non-sentences)
  double averageSentenceLength;
  double

}

class Readability{
  //use different readibility index algorithms on the chapter
}

class Character{
  private boolean isNarrator;
  private boolean isMale;

}
