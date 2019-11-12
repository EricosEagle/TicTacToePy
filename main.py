"""
Module main.py
--------------

This is the main module of the program. It contains the definition of the kivy app and configuration functions.
"""
import os
from src.board import Board

import kivy
from kivy.app import App
from kivy.core.window import Window
kivy.require('1.11.0')


def asset_path(file):
    return os.path.join('assets', file)


class TicTacToeApp(App):
    def config_setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)
        self.title = 'TicTacToePy'
        self.icon = asset_path('icon.png')
        Window.fullscreen = 'auto'

    def build(self):
        self.config_setup()
        return Board()


if __name__ == "__main__":
    TicTacToeApp().run()
