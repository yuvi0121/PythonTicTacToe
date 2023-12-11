import random
import copy
import sys
import time


def get_int(prompt):
    # this lets the player input what the game board's width and height will be
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print ("Oops! Looks like you entered a value of an incorrect format, please enter an integer value...")
            pass


BoardHeight = get_int('How many rows do you want the board to have? (Normally it is 6): ')
# gets the user entered integer value for how many rows the game board should have
BoardWidth  = get_int('How many columns do you want to board to have? (Normally it is 7): ')
# gets the user entered integer value for how many columns the board should have


def main():

    print("""
Welcome to Connect 4!

To win, you must place counters in the board
and make four in a row either vertically,
horizontally or diagonally while not allowing
the enemy player from doing so. Good Luck!
""")
    print()

    while True:
        humansign, computersign = enterHumansign()
        turn = whoGoesFirst()
        print('The %s player won the coin toss and will go first.' % (turn))
        mainBoard = getNewBoard()

        while True:
            if turn == 'human':
                drawBoard(mainBoard)
                move = getHumanMove(mainBoard)
                makeMove(mainBoard, humansign, move)
                if isWinner(mainBoard, humansign):
                    winner = 'human'
                    break
                # 'break' statement is used to immediately exit the if loop and execute the next statement
                turn = 'computer'
            else:
                drawBoard(mainBoard)
                print('The computer player is thinking...')
                time.sleep(2)
                move = getComputerMove(mainBoard, computersign)
                makeMove(mainBoard, computersign, move)
                if isWinner(mainBoard, computersign):
                    winner = 'computer'
                    break
                turn = 'human'

            if isBoardFull(mainBoard):
                winner = 'tie'
                break

        drawBoard(mainBoard)
        print('The winner is: %s' % winner)
        if not playAgain():
            break


def playAgain():
    # this function returns True if the player wants to play again, otherwise it returns False and exits the program
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def enterHumansign():
    # lets the human player input what sign they want to play the game as (either X or O)
    # returns a list with the human player's sign as the first item, and the computer's sign as the second
    sign = ''
    while not (sign == 'X' or sign == 'O'):
        print('Do you want to be player "X" or player "O"?')
        sign = input().upper()

    # the first element will be the human player's sign, the second is the computer's sign
    if sign == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def drawBoard(board):
    # this function draws the game board within python using the values from BoardWidth and BoardHeight
    print()
    print(' ', end='')
    for x in range(1, BoardWidth + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (BoardWidth - 1)))

    for y in range(BoardHeight):
        print('|   |' + ('   |' * (BoardWidth - 1)))

        print('|', end='')
        for x in range(BoardWidth):
            print(' %s |' % board[x][y], end='')
        print()

        print('|   |' + ('   |' * (BoardWidth - 1)))

        print('+---+' + ('---+' * (BoardWidth - 1)))


def getNewBoard():
    board = []
    for x in range(BoardWidth):
        board.append([' '] * BoardHeight)
    return board


def getHumanMove(board):
    # the human player chooses which column to place their counter, while also being able to quit the game
    while True:
        print("""Which column would you like to place your counter?
(1-%s, or type "quit" to quit game and "restart" to restart the game)""" % (BoardWidth))
        move = input()
        if move.lower().startswith('q'):
            # sys.exit to quit the program
            sys.exit()
        if move.lower().startswith('r'):
            # main function is run again to restart the program
            main()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if isValidMove(board, move):
            return move

def getComputerMove(board, computersign):
    potentialMoves = getPotentialMoves(board, computersign, 2)
    bestMoveScore = max([potentialMoves[i] for i in range(BoardWidth) if isValidMove(board, i)])
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveScore:
            bestMoves.append(i)
    return random.choice(bestMoves)


def getPotentialMoves(board, playersign, lookAhead):
    # computer AI, also prevents human from winning by testing human's moves
    if lookAhead == 0:
        return [0] * BoardWidth

    potentialMoves = []

    if playersign == 'X':
        enemysign = 'O'
    else:
        enemysign = 'X'

    # returns (best move, average condition of this state of the game)
    if isBoardFull(board):
        return [0] * BoardWidth

    # figures out the best move to make
    potentialMoves = [0] * BoardWidth
    for playerMove in range(BoardWidth):
        dupeBoard = copy.deepcopy(board)
        # this is where the copy module comes in handy to copy the game board and allow
        # for the algorithm to try different moves before actually making a proper move
        if not isValidMove(dupeBoard, playerMove):
            continue
        makeMove(dupeBoard, playersign, playerMove)
        if isWinner(dupeBoard, playersign):
            potentialMoves[playerMove] = 1
            break
        else:
            # computer does other player's moves and determines which move is the best one
            if isBoardFull(dupeBoard):
                potentialMoves[playerMove] = 0
            else:
                for enemyMove in range(BoardWidth):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, enemyMove):
                        continue
                    makeMove(dupeBoard2, enemysign, enemyMove)
                    if isWinner(dupeBoard2, enemysign):
                        potentialMoves[playerMove] = -1
                        break
                    else:
                        results = getPotentialMoves(dupeBoard2, playersign, lookAhead - 1)
                        potentialMoves[playerMove] += (sum(results) / BoardWidth) / BoardWidth
    return potentialMoves

def whoGoesFirst():
    # randomly chooses a player who will go first, 50/50 chance (like flipping a coin)
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'human'


def makeMove(board, player, column):
    for y in range(BoardHeight-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            return


def isValidMove(board, move):
    # checks whether the move that is being made is valid or not, returns false if the move is invalid
    if move < 0 or move >= (BoardWidth):
        return False

    if board[move][0] != ' ':
        return False

    return True


def isBoardFull(board):
    # checks if the game board is full and returns false if there are spaces, allowing the game to continue
    for x in range(BoardWidth):
        for y in range(BoardHeight):
            if board[x][y] == ' ':
                return False
    return True


def isWinner(board, sign):
    # this checks the horizontal spaces on the game board
    for y in range(BoardHeight):
        for x in range(BoardWidth - 3):
            if board[x][y] == sign and board[x+1][y] == sign and board[x+2][y] == sign and board[x+3][y] == sign:
                return True

    # this checks the vertical spaces on the game board
    for x in range(BoardWidth):
        for y in range(BoardHeight - 3):
            if board[x][y] == sign and board[x][y+1] == sign and board[x][y+2] == sign and board[x][y+3] == sign:
                return True

    # this checks diagonal spaces on the board - bottom left to bottom right, as follows (/)
    for x in range(BoardWidth - 3):
        for y in range(3, BoardHeight):
            if board[x][y] == sign and board[x+1][y-1] == sign and board[x+2][y-2] == sign and board[x+3][y-3] == sign:
                return True

    # this checks diagonal spaces on the board - top left to bottom right, as follows (\)
    for x in range(BoardWidth - 3):
        for y in range(BoardHeight - 3):
            if board[x][y] == sign and board[x+1][y+1] == sign and board[x+2][y+2] == sign and board[x+3][y+3] == sign:
                return True

    return False


def playAgain():
    # Allows the user to play again or exit the program after completing a game
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')



if __name__ == '__main__':
    # also allows the program to run from the command line
    main()
