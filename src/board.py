"""
Module board.py
---------------

Contains the Board class.
This class is the layout used in the TicTacToeApp and contains the game's main functions.
"""
from src.minimax import SimpleBoard, minimax
import sys

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class Board(GridLayout):
    LENGTH = 3
    SYMBOLS = {'computer': 'O', 'human': 'X', 'empty': ''}
    DIFFICULTY = {'baby': 0, 'easy': 2, 'medium': 4,
                  'hard': 6, 'impossible': LENGTH ** 2}

    def __init__(self):
        super().__init__()
        self.cols = self.rows = Board.LENGTH
        self.spacing = 2, 2
        self.first_player = 'human'
        self.depth = Board.DIFFICULTY['hard']
        self.button_list = [[Cell() for _ in range(Board.LENGTH)]
                            for _ in range(Board.LENGTH)]
        self.popup = None
        self.init_buttons()
        self.first_move()

    def init_buttons(self, reset=False):
        """
        Initialises/resets the button objects in self.button_list by doing the following:
        - Binding the on_click function
        - Setting the buttons text value to a blank string
        - Adding the button to the Board
        :return:    None
        """
        for row in self.button_list:
            for button in row:
                button.bind(on_release=self.on_click)
                if reset:
                    button.text = ''
                else:
                    self.add_widget(button)

    def first_move(self):
        """
        Runs the first move if the first player is a computer
        :return:    None
        """
        if self.first_player == 'computer':
            i, j = minimax(SimpleBoard(self.button_list), self.depth)
            self.insert(self.button_list[i][j], Board.SYMBOLS['computer'])

    def on_click(self, touch):
        """
        Places the player's symbol on :touch: and generates a response
        :param touch:   The button that was clicked
        :return:        None
        """
        game_over = self.insert(touch, Board.SYMBOLS['human'])
        if not game_over:
            i, j = minimax(SimpleBoard(self.button_list), self.depth)
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
        board = SimpleBoard(self.button_list)
        has_won = board.has_won()
        is_full = board.is_full()
        title = '{} wins!'.format(symbol) if has_won else None
        title = 'It\'s a tie!' if is_full else title
        if title is not None:
            self.end_message(title)
        return has_won or is_full

    def end_message(self, message):
        """
        Displays an end message and asks user to start a new game or exit
        :param message: The message to display
        :return:        None
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
        button_y.bind(on_release=lambda *args: self.reset())
        buttons.add_widget(button_y)
        button_n = Button(text='No')
        button_n.bind(on_release=lambda *args: sys.exit(0))
        buttons.add_widget(button_n)
        contents.add_widget(buttons)
        return contents

    def reset(self):
        """
        Resets the game, called from end of game popup
        :return:    None
        """
        if self.popup is not None:
            self.popup.dismiss()
        self.disabled = False
        self.init_buttons(reset=True)
        self.first_player = 'computer' if self.first_player != 'computer' else 'human'
        self.first_move()


class Cell(Button):
    pass
