# Global stuff

green = "$"
yellow = "?"
black = "_"


file1 = open("./dict/wordle-answers-alphabetical.txt", "r")
wAnswerSet = file1.read().split()
file1.close()

file2 = open("./dict/wordle-allowed-guesses.txt", "r")
wGuessSet = file2.read().split()
file2.close()


