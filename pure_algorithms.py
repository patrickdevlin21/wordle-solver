# Algorithms

import config
import basicPlayFunctions as bp
import narrowing_word_lists as nwl
import random
from math import log


## This is the silliest algorithm, which just iterates through the wordList and checks each to see if it matches the coloredGuesses

def makeRandomConsistentGuess(coloredGuesses, wordList):
#  possibleGuesses = nwl.getConsistentWords(coloredGuesses, wordList)
  return random.choice(wordList)


def startSmartThenGoRandom(coloredGuesses, wordList, startWords=[]):
  if(len(coloredGuesses) < len(startWords)):
    return startWords[len(coloredGuesses)]
  return random.choice(wordList)



# This takes a list of guesses and a wordList and outputs a dictionary consisting of the following:
#  Each key is a list of coloredGuesses, and the object corresponding to each key is the list of words consistent with that
#
#
#~  Example!
#~   splitIntoWordClasses(["cat"], [all 3-letter words])
#~     this should ouput a dictionary with keys...
#~     ["cat", ["_", "_", "_"]] :  [words-without-CAT]
#~     ["cat", ["$", "_", "_"]] :  ["cob", "cot", "cud", ...]   (c[^at][^at])
#~     ["cat", ["?", "?", "_"]] :  ["ace", "abc", "a.."]   namely...   ([^t]ca)|(ac[^t])|(a[^t]c)
#~     ["cat", ["$", "?", "_"]] :  ["cpa", "cfa", "cha", ...]   (c[^at]a)
#~     et cetera...
def splitIntoWordClasses(guesses, wordList=config.wAnswerSet):
   classesIndexedByColors = {}
   for word in wordList:
     cg = [[g, bp.getColor(g, word)] for g in guesses]
     if str(cg) in classesIndexedByColors:
       classesIndexedByColors[str(cg)].append(word)
     else:
       classesIndexedByColors[str(cg)] = [word]
   return classesIndexedByColors


def getWordClassSizes(guesses, wordList=config.wAnswerSet):
   wC = splitIntoWordClasses(guesses, wordList)
   classSizes = [len(wC[c]) for c in wC]
   return [classSizes.count(i) for i in range(max(classSizes)+1)]

def getStatsOnWordClassSizes(guesses, wordList=config.wAnswerSet):
  #max, average, entropy, (#=1), (#=2)
  wC = splitIntoWordClasses(guesses, wordList)
  wC = [len(wC[c]) for c in wC]
  
  return [max(wC), sum(w**2 for w in wC)/sum(wC), sum(w*log(w, 2) for w in wC)/sum(wC), wC.count(1), 2*wC.count(2)]




##  Running this in hard-mode gives [8332, [1, 131, 999, 919, 207, 47, 9, 2]]
#   RAISE is the best guess if we are guessing from original wordle set, and if we must use a guess from that set
#   Using raise every time IN HARD MODE failed to get the following words quickly:
#   Needed 7: foyer, graze, match, swore, tatty, waste, water, wight, willy
#   Needed 8: goner, watch
#
#   Rerunning those words that didn't do well outside of hard mode, the algorithm does better (as one would expect!)
#   In fact, outside of hard mode, the only word requiring six guesses is BOXER (everything else is done in 5 or fewer).  Haha!

def pickBestEntropy(coloredGuesses, consistentAnswers, hardMode=False, permissibleGuesses=config.wAnswerSet):
  if(len(consistentAnswers) ==1):
    return consistentAnswers[0]
  if(consistentAnswers == config.wAnswerSet):
    return "raise" #This was computed to be the best entropy guess, so just go with that to save time.  In fact, I should maybe flesh out (and cache) the start of this tree!  At least the however-many responses to raise!
  if(hardMode):
    wordsToConsider=consistentAnswers
  else:
    wordsToConsider=permissibleGuesses

  bestSoFar=log(len(consistentAnswers),2)
  bestWord=""
  for g in wordsToConsider:
    L = getStatsOnWordClassSizes([g], consistentAnswers)
#    print(g,L)
    if L[2] < bestSoFar:
#      print("New entropy record!  Old record was: ", bestSoFar, " set by ", bestWord, ".  But the new record is ", L[2], " as set by ", g)
      bestWord = g
      bestSoFar = L[2]
  return bestWord



##  Running this in hard-mode gives [8391, [1, 131, 957, 946, 224, 42, 11, 3]]
#   RAISE is the best guess if we are guessing from original wordle set, and if we must use a guess from that set
#   Using raise every time IN HARD MODE failed to get the following words quickly:
#   Needed 7: foyer, graze, match, pound, shave, swore, tatty, waste, water, wight, willy
#   Needed 8: goner, watch, wound


def pickBestAverageCase(coloredGuesses, consistentAnswers, hardMode=False, permissibleGuesses=config.wAnswerSet):
  if(len(consistentAnswers) ==1):
    return consistentAnswers[0]
  if(consistentAnswers == config.wAnswerSet):
    return "raise" #This was computed to be the best average guess, so just go with that to save time.  In fact, I should maybe flesh out (and cache) the start of this tree!  At least the however-many responses to raise!
  bestSoFar=len(consistentAnswers)
  bestWord=""

  if(hardMode):
    wordsToConsider=consistentAnswers
  else:
    wordsToConsider=permissibleGuesses

  for g in wordsToConsider:
    L = getStatsOnWordClassSizes([g], consistentAnswers)
    if L[1] < bestSoFar:
#      print("New averageCase record!  Old record was: ", bestSoFar, " set by ", bestWord, ".  But the new record is ", L[1], " as set by ", g)
      bestWord = g
      bestSoFar = L[1]
  return bestWord




##  Running this in hard-mode gives [8491, [1, 131, 878, 1006, 239, 47, 11, 2]]
#   RAISE and ARISE are tied as best guesses if we are guessing from original wordle set, and if we must use a guess from that set
#   Using raise every time IN HARD MODE failed to get the following words quickly:
#   Needed 7: foyer, graze, match, shave, swore, tatty, waste, water, willy, winch, wound
#   Needed 8: goner, watch

def pickBestWorstCase(coloredGuesses, consistentAnswers, hardMode=False, permissibleGuesses=config.wAnswerSet):
  if(len(consistentAnswers) ==1):
    return consistentAnswers[0]
  if(consistentAnswers == config.wAnswerSet):
    return "raise" #This was computed to be the best worst case (tied with ARISE), so just go with that to save time.  In fact, I should maybe flesh out (and cache) the start of this tree!  At least the however-many responses to raise!

  bestSoFar=len(consistentAnswers)
  bestWord=""

  if(hardMode):
    wordsToConsider=consistentAnswers
  else:
    wordsToConsider=permissibleGuesses

  for g in wordsToConsider:
    L = getStatsOnWordClassSizes([g], consistentAnswers)
    if L[0] < bestSoFar:
#      print("New worstCase record!  Old record was: ", bestSoFar, " set by ", bestWord, ".  But the new record is ", L[0], " as set by ", g)
      bestWord = g
      bestSoFar = L[0]
  return bestWord
