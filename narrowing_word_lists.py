# reverse search
# this document takes a dictionary, and a list of colored guesses, and it finds all the 

import config
import basicPlayFunctions as bp
import re


def doesThisWordMatch(coloredGuesses, word):
  for [g,c] in coloredGuesses:
    if c!= bp.getColor(g, word):
      return False
  
  return True



## This is the silliest algorithm, which just iterates through the wordList and checks each to see if it matches the coloredGuesses

def getConsistentWords1(coloredGuesses, wordList=config.wAnswerSet):
  return [w for w in wordList if doesThisWordMatch(coloredGuesses, w)]
  

def getConsistentWords(coloredGuesses, wordList=config.wAnswerSet):
  return getConsistentWords1(coloredGuesses, wordList)
  

def getConsistentWords2(coloredGuesses, wordList=config.wAnswerSet):
    newWordList=wordList
    
    for [g,c] in coloredGuesses:
      str1 = ""
      lettersInG = set(g)
      letterCounts = {l : [0,0,0] for l in lettersInG}
      for index, letter in enumerate(g):# First look at the green / non-green letters
        if(c[index] == config.green):
          str1 += letter
          letterCounts[letter][0]+=1
        elif(c[index]==config.yellow):
          letterCounts[letter][1]+=1
          str1 += "[^" + letter + "]"
        else:
          letterCounts[letter][2]+=1
          str1 += "[^" + letter + "]"

#      print(g,c,str1) #str1 is just what matches according to green/non-green letters
      blackLetters = {l for l in lettersInG if letterCounts[l][2]>0}
      yellowLetters = {l for l in lettersInG if letterCounts[l][1]>0}
      greenLetters = {l for l in lettersInG if letterCounts[l][0]>0}

      blackRegexStrings = []
      for L in blackLetters:
        blackRegexStrings.append("^[^" + L +"]*(" +L + "[^" + L + "]*){" + str(letterCounts[L][0]+letterCounts[L][1]) +"}$")    #  should be   ^[^l]*(l[^l]*){k}$  where k is the number of times l shows up as yellow or green
      yellowRegexStrings = []
      for L in yellowLetters:
        yellowRegexStrings.append("^[^" + L +"]*(" +L + "[^" + L + "]*){" + str(letterCounts[L][0]+letterCounts[L][1]) +",}$")    #  should be   ^[^l]*(l[^l]*){k,}$  where k is the number of times l shows up as yellow or green
#      print(g,c,str1, blackRegexStrings, yellowRegexStrings)
      
      r = re.compile(str1)
      newWordList = list(filter(r.match, newWordList))
      for s in blackRegexStrings:
        r = re.compile(s)
        newWordList = list(filter(r.match, newWordList))
      for s in yellowRegexStrings:
        r = re.compile(s)
        newWordList = list(filter(r.match, newWordList))
    return newWordList


## We should be able to streamline the above in a few ways...

#~   I **could** try to do a thing that converts a coloredGuess into a regex string
#  Like...  For each index, we just keep track of what letters it could be.
#  This would be easy for green letters (they say what that spot IS), and it's not impossible to imagine how the rest of it works
#
#  The only other thing is that we also have information of how many of each letter appears in total
#    Like!  We know "there are at least k of LETTER" iff we have a word with k colored LETTER in it
#    And we know "there are at most k of LETTER" iff we have a word with k LETTER in it, at least one of which is not colored
#    And...  I think the info we get from guess to guess is kind of not independent.  I mean, we can't really combine it in any fundamentally new way.  Yea...
#
#
#   SO!  To go from coloredGuesses   to  regex, what we could do is...
#      matchesAll <==> matches each word     (So we only have to go from one word to its regex)
#
#   And! For each colored guess, we can split it into   greenLetters,   yellowLetters,  blackLetters
#    (1)  We must keep the green letters exactly as they are.  (that's easy)
#    (2)  We must insist that each non-green letter doesn't show up in that exact spot of the word
#    (3)  Then for each L in blackLetters, we insist the word has exactly  (#green L + #yellow L) L's.
#    (4)  For each L in yellowLetters, we insist the word has at least (#green L + #yellow L)
#
#  So I'm imagining maybe we first pass through (1) and (2) with something like   [c][^a][^t]
#  Then we want to go through (3) and (4)...  For each, we get a range of how many times L shows up.  Black letters will give us an exact count.  Then we go through yellow letters, which give a lower bound
#   To count times when L shows up exactly 3 times, we go  ^([^L]* [L]){3} [^L]*$
#   To count times when L shows up at least 3 times, we go  ^([^L]* [L]){3,} [^L]*$
#   To do times when L doesn't show up at all, we go ^[^L]*$
