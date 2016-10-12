#HANGMAN
#Created by: Aaron McCartney
#Version: 1


import random

HANGMANPICS = ['''

 +---+
 |   |
     |
     |
     |
     |
=======''', '''

 +---+
 |   |
 0   |
     |
     |
     |
=======''', '''

 +---+
 |   |
 0   |
 |   |
     |
     |
=======''', '''

 +---+
 |   |
 0   |
/|   |
     |
     |
=======''', '''

 +---+
 |   |
 0   |
/|\  |
     |
     |
=======''', '''

 +---+
 |   |
 0   |
/|\  |
/    |
     |
=======''', '''

 +---+
 |   |
 0   |
/|\  |
/ \  |
     |
=======''']

#wordbank words must be longer than two letters
WORDBANK = 'climbing shoes rope harness chalk belay rock stemming smearing gaston lieback rappeling pump campus bouldering onsight flash redpoint carabiner crimp jug sloper'.split()

#get a random word from WORDBANK
def getRandomWord():
    i = random.randint(0, len(WORDBANK)-1)
    return WORDBANK[i]

#print header of game
def header():
    print('\nH A N G M A N \n')
    wordLength = str(len(word))
    print("I'm thinking of a word with " + wordLength + ' letters.')
    print('Can you guess what it is?')

#print the board
def printBoard():
    #print picture of hangman
    print(HANGMANPICS[len(wrongGuesses) + wrongWords] + '\n')

    #print wrong guesses
    print('Wrong Guesses: ', end='')
    for letters in wrongGuesses:
        print(letters + ' ', end='')
    print()

    #print blanks with correctly guessed letters filled in
    blanks = '_' * len(word)
    for i in range(len(word)): #add correctly guessed letters to blanks
        if word[i] in rightGuesses:
            blanks = blanks[:i] + word[i] + blanks[i+1:]
    for i in range(len(blanks)): #add spaces between charactors
        print(blanks[i] + ' ', end='')
    print('\n')

#obtain guess from user
def getGuess():
    guess = '00'
    repeat = True
    guesses = rightGuesses + wrongGuesses #all letter guesses
    
    while repeat:
        repeat = False
        
        while len(guess) != 1 and len(guess) != 2: #always loops at least once. loops until either one letter or a word of the propper length is guessed
            if len(guess) == len(word):
                if guess == word: #check if guess is correct
                    return guess
                return '00'
            elif guess != '00': #check if player guessed a word that's the wrong length
                print('My word is ' + str(len(word)) + ' letters long; ' + guess + ' is ' + str(len(guess)) + ' letters long.')

            print('Guess a letter, or the word: ', end='') #always prints first time in loop
            guess = input().lower()
            
        #check if player already guessed that letter 
        while guess in guesses:
            print('You already guessed that letter. Pick another: ', end='')
            guess = input().lower()
            repeat = True

        #check if value entered is a letter
        while not guess.isalpha():
            print('Please enter a letter: ', end='')
            guess = input().lower()
            repeat = True
            
    return guess

#initiate game
rightGuesses = []
wrongGuesses = []
wrongWords = 0
word = getRandomWord()
repeat = True
initiateGame = False
printBoardBool = True

header()
printBoard()

while(repeat == True):  #loops until player quits  
    #get guess
    guess = getGuess()

    if guess in word: #player guessed correctly
        rightGuesses += guess

        #Check if player won
        won = True
        for i in range(len(word)): 
            if word[i] not in rightGuesses:
                won = False #a letter in the secret word has not been guessed
        if won == True:
            print('You win! The word was ' + word + '.')

            #Play again?
            print('Do you want to play again?')
            while True:
                again = input().lower()
                if again == 'y' or again == 'yes':
                    initiateGame = True
                    break
                elif again == 'n' or again == 'no':
                    repeat = False
                    printBoardBool = False
                    break
                else:
                    print('Yes or NO?')
        
    #player guessed incorectly    
    else:
        if len(guess) == 1: #player guessed a wrong letter
            wrongGuesses += guess
        else:
            wrongWords += 1 #player guessed a wrong word

        #Check if player lost
        if len(wrongGuesses) + wrongWords == len(HANGMANPICS)-1:
            printBoard()
            print('You lose! The word was: ' + word)

            #Play again?
            print('Do you want to play again?')
            while True:
                again = input().lower()
                if again == 'y' or again == 'yes':
                    initiateGame = True
                    break
                elif again == 'n' or again == 'no':
                    repeat = False
                    printBoardBool = False
                    break
                else:
                    print('Yes or NO?')

    #restart game
    if initiateGame == True:
        rightGuesses = []
        wrongGuesses = []
        wrongWords = 0
        word = getRandomWord()
        header()
        initiateGame = False

    if printBoardBool == True: #true unless the player quit
        printBoard()


print('Thanks for playing!') #only prints after player quit
    
        
    

    




    

