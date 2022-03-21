## test algorithms

import config
import basicPlayFunctions as bp
import narrowing_word_lists as nwl
import pure_algorithms as pa
import random
import time


def annotatedSingleTestWithHuman(answer=""):
    if(answer== ""):
      answer= random.choice(config.wAnswerSet) #grab a random answer from the wordle dictionary
      print("Randomly chosen answer is: ", answer)
    answer = answer.lower()
    
    # Display some nice formatting stuff maybe?  Like a header?
    print("The answer has ", len(answer), " letters.  Good luck!")

    guessesThusFar = [] #Initialize this to empty
    keepGoing=True
    
    possibleAnswers = config.wAnswerSet
    
    while(keepGoing):
      print("There are ", len(possibleAnswers), " answers consistent with the info so far.  Of these, I randomly pick: ", random.choice(possibleAnswers))
      if(len(possibleAnswers) < 100):
        print("All possible answers are: ", possibleAnswers)
      
      newGuess = input("Next guess: ")  # Ask user for a word
      while(len(newGuess) != len(answer)): # Later I should add other validation, like checking if the guess is a valid word
        newGuess = input("Sorry.  Please input a guess of the correct length: ") # If newGuess isn't the correct length, make them guess again

      newColor = bp.getColor(newGuess, answer) # Compute how the word did

      guessesThusFar.append([newGuess, newColor])
      for gc in guessesThusFar:
        bp.displayGuessColor(gc[0], gc[1])
      
      possibleAnswers = nwl.getConsistentWords([newGuess], possibleAnswers)
      
      if(newGuess.lower() == answer.lower()): # If word is a match, say they won!
        print("You did it!  Good job.")
        keepGoing = False
      elif(len(guessesThusFar) > 5):
        print("Sorry!  You lost.  The answer was ", answer.upper())
        keepGoing = False
        print("The answers consistent after your last guess were: ", )  


def singleTest(algo, answer="", verbose=False):
    if(answer== ""):
      answer= random.choice(config.wAnswerSet) #grab a random answer from the wordle dictionary
      if(verbose):
        print("Randomly chosen answer is: ", answer)
    answer = answer.lower()
    
    guessesThusFar = [] #Initialize this to empty
    keepGoing=True
    
    possibleAnswers = config.wAnswerSet
    
    while(keepGoing):
      newGuess = algo(guessesThusFar, possibleAnswers)
      if(verbose):
        print("There are ", len(possibleAnswers), " answers consistent with the info so far.  Of these, I pick: ", newGuess)
        if(len(possibleAnswers) < 100):
          print("All possible answers are: ", possibleAnswers)
      
      newColor = bp.getColor(newGuess, answer) # Compute how the word did

      guessesThusFar.append([newGuess, newColor])
#      for gc in guessesThusFar:
#        bp.displayGuessColor(gc[0], gc[1])
      
      possibleAnswers = nwl.getConsistentWords([[newGuess, newColor]], possibleAnswers)
      
      if(newGuess.lower() == answer.lower()): # If word is a match, say they won!
#        print("You did it!  Good job.")
        keepGoing = False
        if(len(guessesThusFar)>6):
          print("This algorithm needed too many guesses.  To guess", answer, "required", len(guessesThusFar), "guesses.")
        return [True, guessesThusFar]
      elif(len(guessesThusFar) > 10):
        print("Sorry!  We lost.  The answer was ", answer.upper())
        keepGoing = False
        return [False, guessesThusFar]
        
        
def testAgainstDictionary(algo, verbose=False, allWords = config.wAnswerSet):
    print("Beginning comprehensive test...")
    stats = []
    for w in allWords:
      [won, guessesUsed] = singleTest(algo, w)
      stats.append([w, won, len(guessesUsed), guessesUsed])
      if((len(stats) % 200 == 0) and verbose):
        print("Now checking:", w, ".  This is word number:", len(stats))
    return stats
    distribution = [s[2] for s in stats]
    return [sum(distribution), [len([d for d in distribution if d==i+1]) for i in range(max(distribution))]]
    return stats
    
    #testAgainstDictionary(lambda c,w: startSmartThenGoRandom(c,w,["louse", "train"]))
    
    


def getStatsForAllWordPairs(verbose=True, allWords = config.wAnswerSet):
    print("Starting stats")
    start = time.time()
    if(verbose):
      print("Getting stats for all word pairs.  This will output a big dictionary indexed by first words.  Each corresponding value will itself be a dictionary indexed by choice of second word.  The values of this inner dictionary are arrays of how many word classes there are of various lengths.  The index L[word]['-1'] is reserved for [g,k] where g is a word g such that guessing word, g yields the most classes of size 1 (and this number is k).")
    L = {}
    for g1 in allWords:
      L[g1] = {} # initialize to empty dictionary
      L[g1]["-1"] = ['', 0]
      bestSoFar = 0
      
      for g2 in allWords:
#        wc=pa.splitIntoWordClasses([g1,g2])
#         wc = pa.getWordClassSizes([g1,g2])
        wc = pa.getStatsOnWordClassSizes([g1, g2], allWords)
        L[g1][g2] = wc
        if(wc[1] > bestSoFar):
          L[g1]["-1"] = [g2, wc[1]]
          bestSoFar = wc[1]
#        if((verbose) and len(L[g1]) % 200 == 1):
#          print("Processing " + g1 + ", and we just compared it with " + g2 + " (which is number", len(L[g1]),").  So far, the best for base word " + g1 + " is ", str(L[g1]["-1"]))

      if((verbose) and len(L) % 2 == 1):
        print("We just finished processing " + g1 + ", which is word number: ", len(L))
        print("Time so far is: ", time.time()-start, " which has average seconds per word equal to: ", (time.time() - start)/len(L))
    return L
    
    
    
def findBestWordWith(startingWord, verbose=True, allWords = config.wAnswerSet):
    print("Starting stats")
    start = time.time()
#    if(verbose):
#      print("Getting stats for all word pairs.  This will output a big dictionary indexed by first words.  Each corresponding value will itself be a dictionary indexed by choice of second word.  The values of this inner dictionary are arrays of how many word classes there are of various lengths.  The index L[word]['-1'] is reserved for [g,k] where g is a word g such that guessing word, g yields the most classes of size 1 (and this number is k).")
    L = {}
    bestSoFar = 0
    bestWord = ""
    for word in allWords:
#       wc=pa.splitIntoWordClasses([g1,g2])
#         wc = pa.getWordClassSizes([g1,g2])
        wc = pa.getStatsOnWordClassSizes([startingWord, word], allWords)
#        wc = list(mySplitLocal([startingWord, word]).values())
#        num1=wc.count(1)
        num1=wc[3]
        L[word] = wc
        if(num1 > bestSoFar):
          bestSoFar = num1
          bestWord = word
#        if((verbose) and len(L[g1]) % 200 == 1):
#          print("Processing " + g1 + ", and we just compared it with " + g2 + " (which is number", len(L[g1]),").  So far, the best for base word " + g1 + " is ", str(L[g1]["-1"]))
    if(verbose):
      print("Best word was " + bestWord + ", which has stats: ", str(L[bestWord]), ".  Time taken: ", time.time()-start)
    return L
    
def findBestWordWith2(startingWord, verbose=True, allWords = config.wAnswerSet):
    print("Starting stats")
    start = time.time()
#    if(verbose):
#      print("Getting stats for all word pairs.  This will output a big dictionary indexed by first words.  Each corresponding value will itself be a dictionary indexed by choice of second word.  The values of this inner dictionary are arrays of how many word classes there are of various lengths.  The index L[word]['-1'] is reserved for [g,k] where g is a word g such that guessing word, g yields the most classes of size 1 (and this number is k).")
    L = {}
    bestSoFar = 0
    bestWord = ""
    L = [[word, pa.getStatsOnWordClassSizes([startingWord, word], allWords)] for word in allWords]
#    bestSoFar = max([x[1][3] for x in L])
    if(verbose):
      print("Time taken: ", time.time()-start)
    return L
