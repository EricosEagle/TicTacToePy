from os.path import join
from board import Board

import kivy
from kivy.app import App
kivy.require('1.11.0')

class TicTacToeApp(App):
    def config_setup(self):
        self.title = 'TicTacToePy'
        self.icon = join('assets', 'icon.png')

    def build(self):
        self.config_setup()
        return Board()

if __name__ == "__main__":
    TicTacToeApp().run()