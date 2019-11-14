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


def asset_path(file):
    return os.path.join('assets', file)


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

    def config_setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)
        self.title = 'TicTacToePy'
        self.icon = asset_path('icon.png')
        Window.fullscreen = 'auto'

    @staticmethod
    def get_sm():
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(PlayMenu(name='play'))
        sm.add_widget(SettingsMenu(name='settings'))
        sm.add_widget(GameScreen(name='sp', game_mode=GameMode.SINGLE_PLAYER))
        sm.add_widget(GameScreen(name='mp', game_mode=GameMode.MULTI_PLAYER))
        return sm

    def build(self):
        self.config_setup()
        return TicTacToeApp.get_sm()


if __name__ == "__main__":
    TicTacToeApp().run()
