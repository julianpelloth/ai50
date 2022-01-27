"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# Implemented by me
def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Check if board is terminal board
    if terminal(board):
        return None
    # Check if board is in the initial state
    if board == initial_state():
        return X

    # Determine how often each player has played
    num_x = 0
    num_o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                num_x = num_x + 1
            if board[i][j] == O:
                num_o = num_o + 1

    if num_o < num_x:
        return O
    else:
        return X


# Implemented by me
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if the board is not a terminal board
    if terminal(board):
        return None

    action = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i, j))

    return action


# Implemented by me
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (i, j) = action
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise NameError('Not a valid action for the given board')
    if board[i][j] is not EMPTY:
        raise NameError('Not a valid action for the given board')

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


# Implemented by me
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]

    return None


# Implemented by me
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Determine if there is a winner
    if winner(board):
        return True

    # Determine if the game is a tie
    tie = True
    for i in range(3):
        for j in range(3):
            tie = tie and (board[i][j] is not EMPTY)

    return tie


# Implemented by me
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    tmp = winner(board)

    if tmp == X:
        return 1
    elif tmp == O:
        return -1
    else:
        return 0


# Implemented by me
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if the board is not a terminal board
    if terminal(board):
        return None

    if player(board) == X:
        (action, util) = getMax(board)
    else:
        (action, util) = getMin(board)

    return action


# Implemented by me
def getMax(board):
    if player(board) is not X:
        return None, -1

    act = actions(board)
    action = act[0]
    util = -1
    for a in act:
        new_board = result(board, a)

        if terminal(new_board):
            u = utility(new_board)
            if util < u:
                util = u
                action = a
        else:
            (x, u) = getMin(new_board)
            if util < u:
                util = u
                action = a

        if util is 1:
            break

    return action, util


# Implemented by me
def getMin(board):
    if player(board) is not O:
        return None, 1

    act = actions(board)
    action = act[0]
    util = 1
    for a in act:
        new_board = result(board, a)

        if terminal(new_board):
            u = utility(new_board)
            if util > u:
                util = u
                action = a
        else:
            (x, u) = getMax(new_board)
            if util > u:
                util = u
                action = a

        if util is -1:
            break

    return action, util

