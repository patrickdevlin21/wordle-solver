import matplotlib.pyplot as plt
import numba
from matplotlib import colors

from IPython.display import clear_output

import colorama
import random

import config






## getColor:
# This takes two strings of the same length (guess and answer) and returns a list of the same length, which is the colors for how the guess should be marked against answer.
#
# Examples:
#   getColor("pizza", "pasta") -->  [g,b,b,b,g]
#   getColor("feast", "farce") -->  [g,y,y,b,b]
#   getColor("dress", "pants") -->  [b,b,b,b,g]
#   getColor("mummy", "dream") -->  [y,b,b,b,b]
#
# A letter is marked green iff the two words agree in that spot.
# A letter is marked yellow iff it should not be marked green, and the letter corresponds to a "free_letter" (defined as follows):
#  The multiset free_letters changes as the program runs. (strictly speaking, it's a word, but we don't actually care about order)
#  Initially free_letters is equal to answer.
#  (0) Letters of answer that match the corresponding indexed letter of guess are not free and must be removed from free_letters.
#  (1) As we process the letters of guess from left-to-right, if we get to a letter that we'll mark yellow, then we must also remove one instance of that letter from free_letters.
#
#~~ As examples...
#  getColor("pizza", "pasta"):
#	after first for loop--> colors=[g,b,b,b,g],  free_letters="ast"
#	after second for loop--> colors=[g,b,b,b,g],  free_letters="ast"
#  getColor("feast", "farce"):
#	after first for loop--> colors=[g,b,b,b,b],  free_letters="arce"
#	after second for loop--> colors=[g,y,y,b,g],  free_letters="rc"
#  getColor("mummy", "dream"):
#	after first for loop--> colors=[b,b,b,b,g],  free_letters="dream"
#	after second for loop--> colors=[y,b,b,b,b],  free_letters="drea"

def getColor(guess, answer):
    guess = guess.lower() # First clean inputs and make sure they're the same length.  These lines can be commented out if we're sure to always pass lowercase inputs of the same length:
    answer = answer.lower()    
    if( len(guess) != len(answer)): # This should never be an issue, but we're checking if the words are the same length or not
        print("Trying to compare ", guess, " to the answer ", answer, ", but the words aren't the same length.")
        return []

    colors = [config.black] * len(guess) # Initializes colors to all black
    free_letters = answer #Intially all letters are free
    
    for index, letter in enumerate(guess): # First go through and color things green
        if(letter==answer[index]): # Found something to mark as green
            colors[index] = config.green
            free_letters=free_letters.replace(letter, "",1) #answer letters corresponding to greens aren't free
            
    for i, letter in enumerate(guess):
        if(colors[i] != config.green): # If letter isn't already green, then we should consider marking it yellow
            if(letter in free_letters): # Found something to mark as yellow
                free_letters=free_letters.replace(letter, "",1) #answer letters corresponding to previously colored yellow letters aren't free
                colors[i] = config.yellow
    return colors


def get_color_coded_str(letter, c):
    letter = letter.upper()
    if (c == config.black):
      return '\x1b[1;37;40m' + letter + '\x1b[0m' # white on black
    elif (c == config.yellow):
      return '\x1b[1;30;43m' + letter + '\x1b[0m' # black on yellow
    elif (c == config.green):
      return '\x1b[1;30;42m' + letter + '\x1b[0m' # black on light green
    else:
      return letter

def displayGuessColor(guess, colors):
    print(*[get_color_coded_str(letter, colors[i]) for i, letter in enumerate(guess)])



def playUserGame(answer=""):
    if(answer== ""):
      answer= random.choice(config.wAnswerSet) #grab a random answer from the wordle dictionary
      print("Randomly chosen answer is: ", answer)
    answer = answer.lower()
    
    # Display some nice formatting stuff maybe?  Like a header?
    print("The answer has ", len(answer), " letters.  Good luck!")

    guessesThusFar = [] #Initialize this to empty
    keepGoing=True
    
    while(keepGoing):
      newGuess = input("Next guess: ")  # Ask user for a word
      while(len(newGuess) != len(answer)): # Later I should add other validation, like checking if the guess is a valid word
        newGuess = input("Sorry.  Please input a guess of the correct length: ") # If newGuess isn't the correct length, make them guess again

      newColor = getColor(newGuess, answer) # Compute how the word did

      guessesThusFar.append([newGuess, newColor])
      for gc in guessesThusFar:
        displayGuessColor(gc[0], gc[1])
      
      if(newGuess.lower() == answer.lower()): # If word is a match, say they won!
        print("You did it!  Good job.")
        keepGoing = False
      elif(len(guessesThusFar) > 5):
        print("Sorry!  You lost.  The answer was ", answer.upper())
        keepGoing = False
        


