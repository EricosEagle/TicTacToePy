from copy import deepcopy
from math import inf as max_score

LENGTH = 3
SYMBOLS = {'computer': 'O', 'human': 'X', 'empty': ''}


class SimpleBoard:
    def __init__(self, board):
        self.__board = [[button.text for button in row] for row in board]

    def __getitem__(self, index):
        return self.__board[index]

    def __len__(self):
        return len(self.__board)

    def __iter__(self):
        return iter(self.__board)

    def is_full(self):
        return not any([symbol == SYMBOLS['empty'] for row in self.__board for symbol in row])

    def has_won(self):
        return abs(evaluate(self)) == max_score


def get_possibilities(board, symbol):
    """
    :param board:   The board to insert :symbol: into
    :param symbol:  The symbol to insert into :board:
    :return:        A list of tuples containing:
                    0 - A copy of :board: with :symbol: inserted into an empty spot
                    1 - The indexes (i and j) where :symbol: was inserted
    """
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == SYMBOLS['empty']:
                option = deepcopy(board)
                option[i][j] = symbol
                out.append((option, (i, j)))
    return out


def evaluate(board):
    """
    :param board:   The board to evaluate
    :return:        :board:'s score based on the number of 2 in a rows
    """
    lines = check_rows(board) + check_cols(board) + check_diags(board)
    two_in_row = [0, 0]
    for line in lines:
        for i in range(len(line)):
            if line[i] == LENGTH:
                return max_score * (-1 if i == 1 else 1)
            if line[i] == LENGTH - 1 and line[1 - i] == 0:
                two_in_row[i] += 1
    comp_score = 10 ** two_in_row[0] if two_in_row[0] > 0 else 0
    player_score = 2 * (10 ** two_in_row[1]) if two_in_row[1] > 0 else 0
    return comp_score - player_score


def check_rows(board):
    """
    :param board:   The game board or a list of rows
    :return:        A list containing how many of each symbol is in each row in :board:
    """
    out = []
    for row in board:
        out.append((row.count(SYMBOLS['computer']), row.count(SYMBOLS['human'])))
    return out


def check_cols(board):
    """
    :param board:   The game board
    :return:        A list containing how many of each symbol is in each column in :board:
    """
    transpose = [[row[i] for row in board] for i in range(LENGTH)]
    return check_rows(transpose)


def check_diags(board):
    """
    :param board:   The game board
    :return:        A list containing how many of each symbol is in each diagonal in :board:
    """
    diagonals = [[board[i][i] for i in range(len(board))],
                 [board[i][LENGTH - i - 1] for i in range(len(board))]]
    return check_rows(diagonals)


def minimax(board, depth):
    """
    :param board:   A simplified version of the current board
    :param depth:   How many moves the function can look ahead
    :return:        The i and j indexes of the best move
    """
    alpha = -max_score
    beta = max_score
    if depth <= 0:
        options = get_possibilities(board, SYMBOLS['computer'])
        return pick_highest(options)
    return make_move(board, 'computer', alpha, beta, depth, depth)


def pick_highest(options):
    """
    :param options: A list of all possible moves
    :return:        The move with the highest rating
    """
    scores = [evaluate(x[0]) for x in options]
    return options[scores.index(max(scores))][1]


def make_move(board, player, alpha, beta, depth, idepth):
    """
    :param board:   A simplified version of the current board
    :param player:  The player the algorithm is playing as (Can only be a key from SYMBOLS)
                    (Note: 'computer' tells the function to maximise and 'human' tells the function to minimise)
    :param alpha:   Lower bound for best_score
    :param beta:    Upper bound for best_score
    :param depth:   How many moves the algorithm can look ahead
    :param idepth:  The initial depth
    :return:        The best score or the index of the best move for :player:
    """
    val = evaluate(board)
    if abs(val) == max_score or depth == 0 or board.is_full():
        return val
    options = get_possibilities(board, SYMBOLS[player])
    n_player = 'computer' if player == 'human' else 'human'
    best_index = options[0][1]
    best_score = make_move(options[0][0], n_player, alpha, beta, depth - 1, idepth)
    for option in options[1:]:
        score = make_move(option[0], n_player, alpha, beta, depth - 1, idepth)
        if better_move(player, score, best_score):
            best_index = option[1]
            best_score = score
        if alpha < best_score and player == 'computer':
            alpha = best_score
        elif beta > best_score and player == 'human':
            beta = best_score
        if beta <= alpha:
            break
    return best_score if depth != idepth else best_index


def better_move(player, score, best_score):
    """
    :param player:      Tells the computer if looking for min or max scores (str, 'human'/'computer')
    :param score:       The new score
    :param best_score:  The previous best score
    :return:            If :score: is better than :best_score:
    """
    return score > best_score if player == 'computer' else score < best_score
