import random, time

#global variables
turn = '?'
symbol = [' ', ' '] #[computersymbol, playersymbol]
board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
play = True
score = [0, 0, 0] #[computer, player, ties]

#print the board
def printBoard():
    print()
    print('    |   |   ')
    print('  %s | %s | %s ' %(board[6], board[7], board[8]))
    print('    |   |   ')
    print(' ---+---+---')
    print('    |   |   ')
    print('  %s | %s | %s ' %(board[3], board[4], board[5]))
    print('    |   |   ')
    print(' ---+---+---')
    print('    |   |   ')
    print('  %s | %s | %s ' %(board[0], board[1], board[2]))
    print('    |   |   ')
    print()

#Ask player if he wants to be X or O
def xOrO():
    print('Do you want to be X or 0?: ', end='')
    player = input().upper()
    while not (player == 'X' or player == 'O'): #loops until player enters a valid choice
        print("Please type 'X' or 'O': ", end='')
        player = input().upper()
    return player

#returns availability of a move
def checkAvailability(move):
    return (board[int(move)] == ' ')

#retrieves player input
def playersTurn():
    print('Choose a space (1-9): ', end='')
    choice = input()
    while True: #loops until player enters a valid choice
        while choice not in '1 2 3 4 5 6 7 8 9'.split():
            print('Please type a number between 1 and 9: ', end='')
            chioce = input()

        choice = int(choice) - 1
        if checkAvailability(choice) == True:
            return choice
        else:
            print('That spot is already filled. Please choose another: ', end='')
            choice = input()

#check if sent move results in a win
def checkForWin(move, symbol):
    #if move is already taken, return false
    if checkAvailability(move) == False:
        return False
    
    boardCopy = list(board) #make a copy of the board
    boardCopy[int(move)] = symbol #make move on copy of board
    #check for win on copy of board
    return ((boardCopy[0]==boardCopy[1]==boardCopy[2]!=' ') or (boardCopy[3]==boardCopy[4]==boardCopy[5]!=' ') or (boardCopy[6]==boardCopy[7]==boardCopy[8]!=' ') or #rows
           (boardCopy[0]==boardCopy[3]==boardCopy[6]!=' ') or (boardCopy[1]==boardCopy[4]==boardCopy[7]!=' ') or (boardCopy[2]==boardCopy[5]==boardCopy[8]!=' ') or  #colums
           (boardCopy[0]==boardCopy[4]==boardCopy[8]!=' ') or (boardCopy[6]==boardCopy[4]==boardCopy[2]!=' '))  #across

#returns the computers move
def computersTurn(computerssymbol):
    #check if there's a move that would make the computer win
    for i in range(len(board)):
        if checkForWin(i, symbol[0]):
            return i
    #else check if there's a move that would make the player win    
    for i in range(len(board)):
        if checkForWin(i, symbol[1]):
            return i

    corners = [0, 2, 6, 8]
    sides = [1, 3, 5, 7]
    random.shuffle(corners)
    random.shuffle(sides)

    #else choose an available corner
    for i in corners:
        if checkAvailability(i) == True:
            return i
    #else choose an available side
    for i in sides:
        if checkAvailability(i) == True:
            return i
    #else choose the middle
    return 5

#checks for a tie
def checkForTie():
    for i in board:
        if i == ' ':
            return False
    return True

#asks if player wants to play again
def playAgain():
    print('Do you want to play again? ', end='')
    choice = input().lower()
    while not (choice == 'yes' or choice == 'y' or choice == 'no' or choice == 'n'):
        print("Please type 'Yes' or 'No': ", end='')
        choice = input().lower()

    return (choice == 'y' or choice == 'yes')

#prints "Hmm..."
def thinking():
    pause = 0.4
    dots = 3
    print('Hmmm', end='')
    for i in range(0, dots):
        print('.', end='')
        time.sleep(pause)

#initializes game
def initalize():
    global turn

    print('\nT I C K - T A C K - T O E')
    printScore()
    
    for i in range(len(board)): #prints board with spaces filled with corresponding numbers
        board[i] = str(i + 1)
    printBoard()
    for i in range(len(board)): #resets board
        board[i] = ' '

    #assign computer and player a symbol
    if symbol[1] == ' ':    
        symbol[1] = xOrO()
        if symbol[1] == 'X':
            symbol[0] = 'O'
        else:
            symbol[0] = 'X' 

    #get whos turn it is
    turn = getTurn()
    if turn == 'computer':
        print("I'll go first this time.")
    else:
        print('You go first this time.')

#returns who's turn it is
def getTurn():
    if turn == '?':
        if random.randint(0, 1) == 0:
            return 'player'
        else:
            return 'computer'
    else:
        return turn

#prints the score
def printScore():
    if play == True:
        print('\nScore:')
    else:
        print('\nFinal Score:')
    print('You: %s Me: %s Ties: %s' %(str(score[1]), str(score[0]), str(score[2])))


while play == True: #loops until player quits
    initalize()
    while True: #loops until game ends
        #computer's turn
        if turn == 'computer':
            #retrive computer's move
            move = computersTurn(symbol[0])
            #check for win
            if checkForWin(move, symbol[0]):
                board[int(move)] = symbol[0]
                thinking()
                printBoard()
                print('I win!')
                score[0] += 1
                if playAgain():
                    turn = 'player'
                    break
                else:
                    play = False
                    break
            #only executes if computer didn't win
            board[int(move)] = symbol[0]
            thinking()
            printBoard()

            #check for tie
            if checkForTie():
                print('Tie!')
                score[2] += 1
                if playAgain():
                    turn = 'player'
                    break
                else:
                    play = False
                    break
                
            turn = 'player'

        #player's turn    
        else:
            #retreive player's move
            move = playersTurn()
            #check for win
            if checkForWin(move, symbol[1]):
                board[move] = symbol[1]
                printBoard()
                print('You win!')
                score[1] += 1
                if playAgain():
                    turn = 'computer'
                    break
                else:
                    play = False
                    break

            #only executes if player didn't win
            board[move] = symbol[1]
            printBoard()

            #check for tie
            if checkForTie():
                print('Tie!')
                score[2] += 1
                if playAgain():
                    turn = 'computer'
                    break
                else:
                    play = False
                    break
                
            turn = 'computer'

#prints after player quits
printScore()
print('\nThanks for playing!')

