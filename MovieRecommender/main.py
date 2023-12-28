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
        self.decision_matrix: Optional[np.array] = None

        # TO REMOVE
        self.not_dominated_points = []
        self.criteria_references1: List[TextInput] = []
        self.criteria_references2: List[TextInput] = []
        self.criteria_weights: List[TextInput] = []
        # TO REMOVE

        self.setup_ui()

    def setup_ui(self) -> None:
        box = self.ids["genres_layout"]

        for i, genre in enumerate(self.genres):
            btn = ToggleButton(text=genre, on_press=lambda btn_, genre_=genre, idx=i: self.select(btn_, genre_, idx))
            box.add_widget(btn)
            self.genres_buttons.append(btn)

        box = self.ids["algorithm_layout"]

        for algorithm in ["TOPSIS", "UTA", "RSM"]:
            btn = Button(text=algorithm, on_press=lambda btn_: self.solve(btn_))
            box.add_widget(btn)

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
        self.decision_matrix = decision_matrix.to_numpy()

    def solve(self, btn: Button) -> None:
        if self.decision_matrix is None:
            return None

        algorithm = btn.text
        criteria = [True, True, False]
        directions = ["max", "max", "min"]
        t1 = time.time()

        if algorithm == "TOPSIS":
            reference = [[float(ref1.text), float(ref2.text)] for ref1, ref2 in zip(self.criteria_references1, self.criteria_references2)]
            weights = [float(w.text) for w in self.criteria_weights]
            rank = topsis(deepcopy(self.decision_matrix), reference, weights)
            self.rank = [p[0] for p in rank[:3]]

        elif algorithm == "UTA":
            rank_indices = UTASTAR(self.decision_matrix, criteria)[:3]
            self.rank = [self.decision_matrix[idx] for idx in rank_indices]

        elif algorithm == "RSM":
            pref = np.array([25, 10, 0])
            pref_qwo = np.array([0, 4, 40])
            self.rank = [p for p in determine_sets(pref, pref_qwo, self.decision_matrix, directions)[:3, :]]

        t2 = time.time()
        print(f"Czas: {(t2 - t1) * 1000} [ms]")
        print(self.rank)

    def display(self):
        pass


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))

        return sm


if __name__ == "__main__":
    MainApp().run()
