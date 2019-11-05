import copy
import sys

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

kivy.require('1.11.0')


class Board(GridLayout):

    MAX_VAL = float('inf')
    LENGTH = 3
    SYMBOLS = {'human': 'X', 'computer': 'O'}    # X - Player, O - Comp
    EMPTY = ''
    DIFFICULTY = {'baby': 0, 'easy': 2, 'medium': 3,
                  'hard': 5, 'impossible': LENGTH ** 2}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = Board.DIFFICULTY['hard']
        self.cols = Board.LENGTH
        self.button_list = [[Button(background_color=(1, 1, 1, 1), font_size=72)
                             for _ in range(Board.LENGTH)] for _ in range(Board.LENGTH)]
        for row in self.button_list:
            for button in row:
                button.bind(on_release=self.on_click)
                self.add_widget(button)

    def on_click(self, touch):
        """
        Places the player's symbol on :touch: and generates a response
        :param touch:   The button that was clicked
        """
        if not self.insert(touch, Board.SYMBOLS['human']):
            board_list = Board.convert(self.button_list)
            i, j = self.minimax(board_list)
            self.insert(self.button_list[i][j], Board.SYMBOLS['computer'])

    def insert(self, button, symbol):
        """
        Places :symbol: on :button: and then checks if the game has ended
        :param button:  The button to place :symbol: on
        :param symbol:  The :symbol: to place
        :param board:   A simplified version of self.button_list
        :return:        If the game has ended
        """
        if button.disabled:
            raise IndexError('This cell already has a value!')
        button.text = symbol
        button.disabled = True
        button.unbind(on_release=self.on_click)
        board = Board.convert(self.button_list)
        has_won = Board.has_won(board)
        is_full = Board.is_full(board)
        if has_won:
            self.end_message('{} wins!'.format(symbol))
        elif is_full:
            self.end_message('It\'s a tie!')
        return has_won or is_full

    @staticmethod
    def is_full(board):
        """
        :param board:   The board to check
        :return:        If board is full
        """
        for row in board:
            for symbol in row:
                if symbol == Board.EMPTY:
                    return False
        return True

    def end_message(self, message):
        """
        Displays an end message and exits the program.
        :param message: The message to display
        """
        self.disabled = True
        popup = Popup(title=message, content=Label(
            text='Click outside to end game.'), size_hint=(0.625, 0.625))
        popup.bind(on_dismiss=sys.exit)
        popup.open()

    @staticmethod
    def has_won(board):
        """
        :param board:   The board to check
        :return:        If one of the players has won
        """
        return abs(Board.evaluate(board)) == Board.MAX_VAL

    def minimax(self, board, depth=None):
        """
        :param board:   A simplified version of the current board
        :param depth:   How many moves the function can look ahead
        :return:        The i and j indexes of the best move
        """
        if depth == None:
            depth = self.depth
        options = Board.get_possibilities(board, Board.SYMBOLS['computer'])
        if depth <= 0:
            return Board.pick_highest(options)
        best_board = options[0]
        best_score = Board.play(best_board[0], 'human', depth - 1)
        for i in range(1, len(options)):
            score = Board.play(options[i][0], 'human', depth - 1)
            if Board.better_move('computer', score, best_score):
                best_board = options[i]
                best_score = score
        return best_board[1]

    @staticmethod
    def pick_highest(options):
        """
        :param options: A list of all possible moves
        :return:        The move with the highest rating
        """
        scores = [Board.evaluate(x[0]) for x in options]
        return options[scores.index(max(scores))][1]

    @staticmethod
    def play(board, player, depth):
        """
        :param board:   A simplified version of the current board
        :param player:  The player the algorithm is playing as (Can only be a key from Board.SYMBOLS)
        :param depth:   How many moves the algorithm can look ahead
        :return:        A tuple containing the best score for the player and the depth level it reached
        """
        val = Board.evaluate(board)
        if abs(val) == Board.MAX_VAL or depth <= 0 or Board.is_full(board):
            return (val, depth)
        options = Board.get_possibilities(board, Board.SYMBOLS[player])
        n_player = 'computer' if player == 'human' else 'human'
        best_score = Board.play(options[0][0], n_player, depth - 1)
        for option in options[1:]:
            score = Board.play(option[0], n_player, depth - 1)
            if Board.better_move(player, score, best_score):
                best_score = score
        return best_score

    @staticmethod
    def better_move(player, score, best_score):
        """
        :param player:      Tells the computer if looking for min or max scores (str, 'human'/'computer')
        :param score:       The new score
        :param best_score:  The previous best score
        :return:            If :score: is better than :best_score:
        """
        better_score = score[0] > best_score[0] if player == 'computer' else score[0] < best_score[0]
        better_depth = score[1] > best_score[1] if score[0] == best_score[0] else False
        return better_score or better_depth

    @staticmethod
    def evaluate(board):
        """
        :param board:   The board to evaluate
        :return:        :board:'s score based on the number of 2 in a rows
        """
        lines = Board.check_rows(
            board) + Board.check_cols(board) + Board.check_diags(board)
        two_in_row = [0, 0]
        for line in lines:
            for i in range(len(line)):
                if line[i] == Board.LENGTH:
                    return Board.MAX_VAL * (-1 if i == 1 else 1)
                if line[i] == Board.LENGTH - 1 and line[1 - i] == 0:
                    two_in_row[i] += 1
        comp_score = 10 ** two_in_row[0] if two_in_row[0] > 0 else 0
        player_score = -(10 ** (two_in_row[1] + 1)) if two_in_row[1] > 0 else 0
        return comp_score + player_score

    @staticmethod
    def check_rows(board):
        """
        :param board:   The board or a list of rows
        :return:        A list containing how many of each symbol is in each row in :board:
        """
        out = []
        for row in board:
            out.append(
                (row.count(Board.SYMBOLS['computer']), row.count(Board.SYMBOLS['human'])))
        return out

    @staticmethod
    def check_cols(board):
        """
        :param board:   The game board
        :return:        A list containing how many of each symbol is in each column in :board:
        """
        transpose = [[row[i] for row in board] for i in range(Board.LENGTH)]
        return Board.check_rows(transpose)

    @staticmethod
    def check_diags(board):
        """
        :param board:   The game board
        :return:        A list containing how many of each symbol is in each diagonal in :board:
        """
        diagonals = [[board[i][i] for i in range(len(board))],
                     [board[i][Board.LENGTH - i - 1] for i in range(len(board))]]
        return Board.check_rows(diagonals)

    @staticmethod
    def convert(board):
        """
        :param board:   A list of all the buttons in the board
        :return:        A simplified version of :board: containng the text values of the buttons
        """
        out = [[button.text for button in row] for row in board]
        return out

    @staticmethod
    def get_possibilities(board, symbol):
        """
        :param board:   The board to insert :symbol: into
        :param symbol:  The symbol to insert into :board:
        :return:        A list of tuples containing:
                        0 - A copy of :board: with symbol inserted into an empty spot
                        1 - The indexes (i and j) where :symbol: was inserted
        """
        out = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == Board.EMPTY:
                    option = copy.deepcopy(board)
                    option[i][j] = symbol
                    out.append((option, (i, j)))
        return out


class TicTacToeApp(App):
    def build(self):
        self.title = 'TicTacToePy'
        return Board()


if __name__ == "__main__":
    TicTacToeApp().run()
