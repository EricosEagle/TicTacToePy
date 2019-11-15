"""
Module main.py
--------------

This is the main module of the program. It contains the definition of the kivy app and configuration functions.
"""
import os
from src.board import Board, GameMode
from src.minimax import Player

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
kivy.require('1.11.0')


# TODO: Set up options menu


class MainMenu(Screen):
    pass


class PlayMenu(Screen):
    pass


class SettingsMenu(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name=kwargs['name'])
        self.add_widget(Board(game_mode=kwargs.get('game_mode', GameMode.SINGLE_PLAYER),
                              first_player=kwargs.get('first_player', Player.HUMAN),
                              difficulty=kwargs.get('difficulty', 'hard')))


class TicTacToeApp(App):

    __sm = None

    def config_setup(self):
        """
        Configures the program
        :return:    None
        """
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)
        self.title = 'TicTacToePy'
        self.icon = os.path.join('assets', 'icon.png')
        Window.fullscreen = 'auto'

    @staticmethod
    def get_sm():
        """
        Generates the screen manager if it is None and returns it
        :return:    The program's ScreenManager
        """
        if TicTacToeApp.__sm is None:
            TicTacToeApp.__sm = ScreenManager(transition=SlideTransition())
            TicTacToeApp.__sm.add_widget(MainMenu(name='menu'))
            TicTacToeApp.__sm.add_widget(PlayMenu(name='play'))
            TicTacToeApp.__sm.add_widget(SettingsMenu(name='settings'))
            TicTacToeApp.__sm.add_widget(GameScreen(name='sp', game_mode=GameMode.SINGLE_PLAYER))
            TicTacToeApp.__sm.add_widget(GameScreen(name='mp', game_mode=GameMode.MULTI_PLAYER))
        return TicTacToeApp.__sm

    def build(self):
        self.config_setup()
        return TicTacToeApp.get_sm()


if __name__ == "__main__":
    TicTacToeApp().run()
