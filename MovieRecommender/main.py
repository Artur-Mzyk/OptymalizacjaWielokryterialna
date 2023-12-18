#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from preprocessing import get_top_movies

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
import time

from typing import List, Tuple, Union


Builder.load_file("layout.kv")


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self) -> None:
        pass

    def get_top_movies(self) -> None:
        genre = self.ids["genre"].text
        n_movies = int(self.ids["n_movies"].text)
        movies = get_top_movies(genre, n_movies)
        self.ids["top_movies_list"].text = "\n".join([f"Title: {v}, ID: {k}" for k, v in movies.items()])


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))

        return sm


if __name__ == "__main__":
    MainApp().run()
