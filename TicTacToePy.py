from copy import deepcopy
from math import inf as max_score
from sys import exit as sysexit

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

kivy.require('1.11.0')

'''
------------------- CHANGELOG -------------------
--------------------- v1.02 ---------------------
Added:
    - Added detailed changelog
    - Added spacing between buttons
Changed:
    - Increased font size
    - Changed background color to white
    - Starting player is now changed with every new game
--------------------- v1.01 ---------------------
Added:
    - Added .kv file
    - Added reset prompt at the end of the game
    - Implemented alpha-beta pruning
Changed:
    - Made code more readable
    - Converted minimax() into a wrapper for play()
    - Updated UI
Removed:
    - Removed unnecessary depth check
--------------------- v1.0 ----------------------
- Created main game with basic features
-------------------------------------------------
'''

class Board(GridLayout):

    LENGTH = 3
    SYMBOLS = {'computer': 'O', 'human': 'X', 'empty': ''}
    DIFFICULTY = {'baby': 0, 'easy': 2, 'medium': 4,
                  'hard': 6, 'impossible': LENGTH ** 2}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_player = 'human'
        self.cols = Board.LENGTH
        self.spacing = 2, 2
        self.depth = Board.DIFFICULTY['impossible']
        self.button_list = [[Cell() for _ in range(Board.LENGTH)]
                            for _ in range(Board.LENGTH)]
        self.popup = None
        for row in self.button_list:
            for button in row:
                button.bind(on_release=self.on_click)
                self.add_widget(button)
        if self.first_player == 'computer':
            i, j = self.minimax(Board.convert(self.button_list))
            self.insert(self.button_list[i][j], Board.SYMBOLS['computer'])

    def on_click(self, touch):
        """
        Places the player's symbol on :touch: and generates a response
        :param touch:   The button that was clicked
        """
        game_over = self.insert(touch, Board.SYMBOLS['human'])
        if not game_over:
            i, j = self.minimax(Board.convert(self.button_list))
            self.insert(self.button_list[i][j], Board.SYMBOLS['computer'])

    def insert(self, button, symbol):
        """
        Places :symbol: on :button: and then checks if the game has ended
        :param button:  The button to place :symbol: on
        :param symbol:  The :symbol: to place
        :return:        If the game has ended
        """
        button.text = symbol
        button.color = (0, 0, 1, 1) if symbol == Board.SYMBOLS['computer'] else (1, 0, 0, 1)
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
                if symbol == Board.SYMBOLS['empty']:
                    return False
        return True

    def end_message(self, message):
        """
        Displays an end message and asks user to start a new game or exit
        :param message: The message to display
        """
        self.disabled = True
        self.popup = Popup(title=message,
                            content=self.popup_contents(), 
                            size_hint=(0.625, 0.625), 
                            auto_dismiss=False)
        self.popup.open()

    def popup_contents(self):
        """
        Generates the contents for the end of game popup
        :return:    The popup's contents
        """
        contents = BoxLayout(orientation='vertical')
        contents.add_widget(Label(text='Would you like to play again?'))
        buttons = BoxLayout(orientation='horizontal')
        button_y = Button(text='Yes')
        button_y.bind(on_release=self.reset)
        buttons.add_widget(button_y)
        button_n = Button(text='No')
        button_n.bind(on_release=sysexit)
        buttons.add_widget(button_n)
        contents.add_widget(buttons)
        return contents

    def reset(self, touch):
        """
        Resets the game, called from end of game popup
        """
        for row in self.button_list:
            for button in row:
                button.text = ''
                button.bind(on_release=self.on_click)
        self.disabled = False
        if self.popup:
            self.popup.dismiss()
        self.first_player = 'computer' if self.first_player != 'computer' else 'human'
        if self.first_player == 'computer':
            i, j = self.minimax(Board.convert(self.button_list))
            self.insert(self.button_list[i][j], Board.SYMBOLS['computer'])

    @staticmethod
    def has_won(board):
        """
        :param board:   The board to check
        :return:        If one of the players has won
        """
        return abs(Board.evaluate(board)) == max_score

    def minimax(self, board):
        """
        :param board:   A simplified version of the current board
        :param depth:   How many moves the function can look ahead
        :return:        The i and j indexes of the best move
        """
        alpha = -max_score
        beta = max_score
        depth = self.depth
        if depth <= 0:
            options = Board.get_possibilities(board, Board.SYMBOLS['computer'])
            return Board.pick_highest(options)
        return Board.play(board, 'computer', alpha, beta, depth, depth)

    @staticmethod
    def pick_highest(options):
        """
        :param options: A list of all possible moves
        :return:        The move with the highest rating
        """
        scores = [Board.evaluate(x[0]) for x in options]
        return options[scores.index(max(scores))][1]

    @staticmethod
    def play(board, player, alpha, beta, depth, idepth):
        """
        :param board:   A simplified version of the current board
        :param player:  The player the algorithm is playing as (Can only be a key from Board.SYMBOLS)
                        (Note: 'computer' tells the function to maximise and 'human' tells the function to minimise)
        :param alpha:   Lower bound for best_score
        :param beta:    Upper bound for best_score
        :param depth:   How many moves the algorithm can look ahead
        :param idepth:  The initial depth
        :return:        The best score or the index of the best move for :player:
        """
        val = Board.evaluate(board)
        if abs(val) == max_score or depth == 0 or Board.is_full(board):
            return val
        options = Board.get_possibilities(board, Board.SYMBOLS[player])
        n_player = 'computer' if player == 'human' else 'human'
        best_index = options[0][1]
        best_score = Board.play(options[0][0], n_player, alpha, beta, depth - 1, idepth)
        for option in options[1:]:
            score = Board.play(option[0], n_player, alpha, beta, depth - 1, idepth)
            if Board.better_move(player, score, best_score):
                best_index = option[1]
                best_score = score
            if alpha < best_score and player == 'computer':
                alpha = best_score
            elif beta > best_score and player == 'human':
                beta = best_score
            if beta <= alpha:
                break
        return best_score if depth != idepth else best_index

    @staticmethod
    def better_move(player, score, best_score):
        """
        :param player:      Tells the computer if looking for min or max scores (str, 'human'/'computer')
        :param score:       The new score
        :param best_score:  The previous best score
        :return:            If :score: is better than :best_score:
        """
        return score > best_score if player == 'computer' else score < best_score

    @staticmethod
    def evaluate(board):
        """
        :param board:   The board to evaluate
        :return:        :board:'s score based on the number of 2 in a rows
        """
        lines = Board.check_rows(board) + Board.check_cols(board) + Board.check_diags(board)
        two_in_row = [0, 0]
        for line in lines:
            for i in range(len(line)):
                if line[i] == Board.LENGTH: 
                    return max_score * (-1 if i == 1 else 1)
                if line[i] == Board.LENGTH - 1 and line[1 - i] == 0:
                    two_in_row[i] += 1
        comp_score = 10 ** two_in_row[0] if two_in_row[0] > 0 else 0
        player_score = 2 * (10 ** two_in_row[1]) if two_in_row[1] > 0 else 0
        return comp_score - player_score

    @staticmethod
    def check_rows(board):
        """
        :param board:   The game board or a list of rows
        :return:        A list containing how many of each symbol is in each row in :board:
        """
        out = []
        for row in board:
            out.append((row.count(Board.SYMBOLS['computer']), row.count(Board.SYMBOLS['human'])))
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
                        0 - A copy of :board: with :symbol: inserted into an empty spot
                        1 - The indexes (i and j) where :symbol: was inserted
        """
        out = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == Board.SYMBOLS['empty']:
                    option = deepcopy(board)
                    option[i][j] = symbol
                    out.append((option, (i, j)))
        return out

class Cell(Button):
    pass

class TicTacToeApp(App):
    def build(self):
        self.title = 'TicTacToePy'
        return Board()

if __name__ == "__main__":
    TicTacToeApp().run()