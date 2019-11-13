"""
Module minimax.py
-----------------

This module contains the SimpleBoard class and all AI Functions
"""
from copy import deepcopy
from enum import Enum
from math import inf


class Player(Enum):
    COMPUTER = 'O'
    HUMAN = 'X'
    EMPTY = ''


class SimpleBoard:

    MAX_SCORE = 10000

    def __init__(self, board):
        self.__board = [[button.text for button in row] for row in board]

    def __getitem__(self, index):
        return self.__board[index]

    def __len__(self):
        return len(self.__board)

    def __iter__(self):
        return iter(self.__board)

    def is_full(self):
        return not any([symbol == Player.EMPTY.value for row in self.__board for symbol in row])

    def has_won(self):
        return abs(evaluate(self)) == SimpleBoard.MAX_SCORE


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
            if board[i][j] == Player.EMPTY.value:
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
            if line[i] == len(board):
                return SimpleBoard.MAX_SCORE * (-1 if i == 1 else 1)
            if line[i] == len(board) - 1 and line[1 - i] == 0:
                two_in_row[i] += 1
    comp_score = 10 * two_in_row[0]
    player_score = 1.5 * 10 * two_in_row[1]
    return comp_score - player_score


def check_rows(board):
    """
    :param board:   The game board or a list of rows
    :return:        A list containing how many of each symbol is in each row in :board:
    """
    out = []
    for row in board:
        out.append((row.count(Player.COMPUTER.value), row.count(Player.HUMAN.value)))
    return out


def check_cols(board):
    """
    :param board:   The game board
    :return:        A list containing how many of each symbol is in each column in :board:
    """
    transpose = [[row[i] for row in board] for i in range(len(board))]
    return check_rows(transpose)


def check_diags(board):
    """
    :param board:   The game board
    :return:        A list containing how many of each symbol is in each diagonal in :board:
    """
    diagonals = [[board[i][i] for i in range(len(board))],
                 [board[i][len(board) - i - 1] for i in range(len(board))]]
    return check_rows(diagonals)


def minimax(board, depth):
    """
    :param board:   The current gamestate
    :param depth:   How many moves the function can look ahead
    :return:        The i and j indexes of the best move
    """
    alpha = -inf
    beta = inf
    if depth <= 0:
        return pick_highest(board)
    return make_move(board, Player.COMPUTER, alpha, beta, depth, depth)


def pick_highest(board):
    """
    :param board:   The current gamestate
    :return:        The move with the highest rating
    """
    options = get_possibilities(board, Player.COMPUTER.value)
    scores = [evaluate(x[0]) for x in options]
    return options[scores.index(max(scores))][1]


def make_move(board, player, alpha, beta, depth, idepth):
    """
    :param board:   A simplified version of the current board
    :param player:  The player the algorithm is playing as (Can only be an instance of Player)
                    (Note: the function maximises for the computer and minimises for the player)
    :param alpha:   Lower bound for best_score
    :param beta:    Upper bound for best_score
    :param depth:   How many moves the algorithm can look ahead
    :param idepth:  The initial depth
    :return:        The best score or the index of the best move for :player:
    """
    val = evaluate(board)
    if abs(val) == SimpleBoard.MAX_SCORE:
        return val * (depth + 1)
    if depth == 0 or board.is_full():
        return val
    options = get_possibilities(board, player.value)
    n_player = Player.COMPUTER if player == Player.HUMAN else player.HUMAN
    best_index = options[0][1]
    best_score = make_move(options[0][0], n_player, alpha, beta, depth - 1, idepth)
    for option in options[1:]:
        score = make_move(option[0], n_player, alpha, beta, depth - 1, idepth)
        if better_move(player, score, best_score):
            best_index = option[1]
            best_score = score
        if alpha < best_score and player == Player.COMPUTER:
            alpha = best_score
        elif beta > best_score and player == Player.HUMAN:
            beta = best_score
        if beta <= alpha:
            break
    return best_score if depth != idepth else best_index


def better_move(player, score, best_score):
    """
    :param player:      Tells the computer if looking for min or max scores (str, Player.HUMAN/Player.COMPUTER)
    :param score:       The new score
    :param best_score:  The previous best score
    :return:            If :score: is better than :best_score:
    """
    return score > best_score if player == Player.COMPUTER else score < best_score
