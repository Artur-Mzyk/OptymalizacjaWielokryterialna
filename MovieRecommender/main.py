#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

from UTA import UTASTAR
from TOPSIS import topsis
from RSM import determine_sets
from copy import deepcopy
from visualization import plot_results

from kivy.graphics import Line, Color, Point
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


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
        self.decision_matrix: Optional[np.ndarray] = None
        self.rank: Optional[np.ndarray] = None

        # self.not_dominated_points = []

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
            self.ids["top_movies_list"].text = f"Downloading data for genre: {genre}"
            movies.extend(self.query.get_top_movies(genre, n_movies))

        if not movies:
            return None

        decision_matrix = construct_decision_matrix(movies, release_year, cast)
        self.ids["top_movies_list"].text = decision_matrix.to_string()
        self.decision_matrix = decision_matrix.to_numpy()

    def solve(self, algorithm: str) -> None:
        if self.decision_matrix is None:
            return None

        criteria = [True, True, False]
        directions = ["max", "max", "min"]
        t1 = time.time()

        if algorithm == "TOPSIS":
            try:
                cast_ref1 = float(self.ids["cast_ref1"].text)
                cast_ref2 = float(self.ids["cast_ref2"].text)
                cast_weight = float(self.ids["cast_weight"].text)
                rating_ref1 = float(self.ids["rating_ref1"].text)
                rating_ref2 = float(self.ids["rating_ref2"].text)
                rating_weight = float(self.ids["rating_weight"].text)
                release_year_ref1 = float(self.ids["release_year_ref1"].text)
                release_year_ref2 = float(self.ids["release_year_ref2"].text)
                release_year_weight = float(self.ids["release_year_weight"].text)

            except ValueError as e:
                self.ids["top_movies_list"].text = str(e)

                return None

            # reference = [[cast_ref1, cast_ref2], [rating_ref1, rating_ref2], [release_year_ref1, release_year_ref2]]
            weights = [cast_weight, rating_weight, release_year_weight]
            decision_matrix = [list(row) for row in self.decision_matrix]
            print(decision_matrix)
            # print(reference)
            print(weights)
            rank_tops = topsis(decision_matrix, directions, weights)
            rank_indices = [r[0] for r in rank_tops]
            self.rank = [self.decision_matrix[idx] for idx in rank_indices]

        elif algorithm == "UTA":
            rank_indices = UTASTAR(self.decision_matrix, criteria)[:3]
            self.rank = [self.decision_matrix[idx] for idx in rank_indices]

        elif algorithm == "RSM":
            try:
                cast_ref1 = float(self.ids["cast_ref1"].text)
                cast_ref2 = float(self.ids["cast_ref2"].text)
                rating_ref1 = float(self.ids["rating_ref1"].text)
                rating_ref2 = float(self.ids["rating_ref2"].text)
                release_year_ref1 = float(self.ids["release_year_ref1"].text)
                release_year_ref2 = float(self.ids["release_year_ref2"].text)

            except ValueError as e:
                self.ids["top_movies_list"].text = str(e)

                return None

            pref = np.array([cast_ref2, rating_ref2, release_year_ref2])
            pref_qwo = np.array([cast_ref1, rating_ref1, release_year_ref1])
            self.rank = [p for p in determine_sets(pref, pref_qwo, self.decision_matrix, directions)[:3, :]]

        t2 = time.time()
        self.ids["time"].text = f"Czas: {int((t2 - t1) * 1000)} [ms]"
        print(self.rank)
        print(self.ids["top_movies_list"].text)

    def display(self):
        if self.rank is None:
            return None

        box = self.ids["plot_layout"]

        for child in box.children:
            box.remove_widget(child)

        fig = plot_results([list(row) for row in self.decision_matrix], self.rank)
        plot_widget = FigureCanvasKivyAgg(figure=fig)
        box.add_widget(plot_widget)


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))

        return sm


if __name__ == "__main__":
    MainApp().run()
