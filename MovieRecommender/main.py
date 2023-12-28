#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

from preprocessing import Query

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

from typing import List, Tuple, Union, Optional, Dict
from imdb import Movie


def construct_decision_matrix(movies: List[Movie.Movie], release_year: int, cast: str) -> pd.DataFrame:
    """
    Function to construct decision matrix
    :param movies:
    :param release_year:
    :param cast:
    :return:
    """

    data: Dict[str, List[Union[int, float, str]]] = {"title": [], "present_cast": [], "rating": [], "release_year_diff": []}

    for movie in movies:
        data["title"].append(movie["title"])
        data["present_cast"].append(sum([1 for person in movie["cast"] if person["name"] in cast]))
        data["rating"].append(movie["rating"])
        data["release_year_diff"].append(abs(movie["year"] - release_year))

    decision_matrix = pd.DataFrame(data)
    decision_matrix.set_index("title", inplace=True)

    return decision_matrix


Builder.load_file("layout.kv")


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.query = Query()
        self.genres: List[str] = self.query.get_genres()
        self.genres_buttons: List[CheckBox] = []
        self.numbers_widgets: List[Optional[Tuple[Label, TextInput]]] = [None for _ in range(len(self.genres))]
        self.setup_ui()

    def setup_ui(self) -> None:
        box = self.ids["genres_layout"]

        for i, genre in enumerate(self.genres):
            btn = ToggleButton(text=genre, on_press=lambda btn_, genre_=genre, idx=i: self.select(btn_, genre_, idx))
            box.add_widget(btn)
            self.genres_buttons.append(btn)

    def select(self, btn: ToggleButton, genre: str, idx: int) -> None:
        box = self.ids["numbers_layout"]

        if btn.state == "down":
            box.rows += 1
            lbl = Label(text=genre, color="black")
            box.add_widget(lbl)
            inp = TextInput()
            box.add_widget(inp)
            self.numbers_widgets[idx] = (lbl, inp)

        else:
            lbl, inp = self.numbers_widgets[idx]
            self.numbers_widgets[idx] = None
            box.remove_widget(lbl)
            box.remove_widget(inp)
            box.rows -= 1

    def get_top_movies(self) -> None:
        selected_genres: List[Tuple[str, int]] = []

        try:
            release_year = int(self.ids["release_year"].text)

        except ValueError as e:
            self.ids["top_movies_list"].text = str(e)

            return None

        for i, btn in enumerate(self.genres_buttons):
            if btn.state == "normal":
                continue

            try:
                genre = self.numbers_widgets[i][0].text
                n_movies = int(self.numbers_widgets[i][1].text)
                selected_genres.append((genre, n_movies))

            except ValueError as e:
                self.ids["top_movies_list"].text = str(e)

                return None

        cast = self.ids["cast"].text
        movies: List[Movie.Movie] = []

        for genre, n_movies in selected_genres:
            movies.extend(self.query.get_top_movies(genre, n_movies))

        decision_matrix = construct_decision_matrix(movies, release_year, cast)
        self.ids["top_movies_list"].text = decision_matrix.to_string()


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))

        return sm


if __name__ == "__main__":
    MainApp().run()
