import os
from src.board import Board

import kivy
from kivy.app import App
kivy.require('1.11.0')


def asset_path(file):
    return os.path.join('assets', file)


class TicTacToeApp(App):
    def config_setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(os.path.join(path, '..'))
        self.title = 'TicTacToePy'
        self.icon = asset_path('icon.png')

    def build(self):
        self.config_setup()
        return Board()


if __name__ == "__main__":
    TicTacToeApp().run()
