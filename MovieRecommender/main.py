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


def construct_decision_matrix(movies: List[Movie.Movie], cast_popularity: List[int], writer: str, release_year: int,
                              cast: str) -> pd.DataFrame:
    """
    Function to construct decision matrix
    :param movies:
    :param cast_popularity:
    :param writer:
    :param release_year:
    :param cast:
    :return:
    """

    data: Dict[str, List[Union[int, float, str]]] = {"title": [], "writer": [], "present_cast": [],
                                                     "cast_popularity": [], "rating": [], "release_year_diff": [],
                                                     "special_effects": []}

    for i, movie in enumerate(movies):
        if movie["title"] in data["title"]:
            continue

        data["title"].append(movie["title"])
        data["writer"].append(sum([1 for person in movie["writer"] if "name" in person.keys() and person["name"] in writer]))
        data["present_cast"].append(sum([1 for person in movie["cast"] if person["name"] in cast]))
        data["cast_popularity"].append(cast_popularity[i])
        data["rating"].append(movie["rating"])
        data["release_year_diff"].append(abs(movie["year"] - release_year))
        data["special_effects"].append(len(movie["special effects"]))

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
        self.decision_matrix_df: Optional[pd.DataFrame] = None
        self.rank: Optional[np.ndarray] = None
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
            self.ids["exception_layout"].text = str(e)

            return None

        for i, btn in enumerate(self.genres_buttons):
            if btn.state == "normal":
                continue

            try:
                genre = self.numbers_widgets[i][0].text
                n_movies = int(self.numbers_widgets[i][1].text)
                selected_genres.append((genre, n_movies))

            except ValueError as e:
                self.ids["exception_layout"].text = str(e)

                return None

        writer = self.ids["writer"].text
        cast = self.ids["cast"].text
        movies: List[Movie.Movie] = []

        for genre, n_movies in selected_genres:
            movies.extend(self.query.get_top_movies(genre, n_movies))

        if not movies:
            return None

        cast_popularity: List[int] = [self.query.get_cast_popularity(movie["cast"][0].personID) for movie in movies]
        self.decision_matrix_df = construct_decision_matrix(movies, cast_popularity, writer, release_year, cast)
        self.decision_matrix = self.decision_matrix_df.to_numpy()
        self.ids["exception_layout"].text = "Downloaded"
        print(self.decision_matrix)

    def solve(self, algorithm: str) -> None:
        if self.decision_matrix is None:
            return None

        criteria = [True, True, True, True, False, True]
        directions = ["max", "max", "max", "max", "min", "max"]
        t1 = time.time()

        try:
            writer_weight = float(self.ids["writer_weight"].text)
            cast_weight = float(self.ids["cast_weight"].text)
            cast_popularity_weight = float(self.ids["cast_weight"].text)
            rating_weight = float(self.ids["rating_weight"].text)
            release_year_weight = float(self.ids["release_year_weight"].text)
            special_effects_weight = float(self.ids["special_effects_weight"].text)

        except ValueError as e:
            self.ids["exception_layout"].text = str(e)

            return None

        if algorithm == "TOPSIS":
            weights = [writer_weight, cast_weight, cast_popularity_weight, rating_weight, release_year_weight,
                       special_effects_weight]
            decision_matrix = [list(row) for row in self.decision_matrix]
            rank_tops = topsis(decision_matrix, directions, weights)
            rank_indices = [r[0] for r in rank_tops]
            self.rank = [self.decision_matrix[idx] for idx in rank_indices]

        elif algorithm == "UTA":
            rank_indices = UTASTAR(self.decision_matrix, criteria)[:3]
            self.rank = [self.decision_matrix[idx] for idx in rank_indices]

        elif algorithm == "RSM":
            pref = np.array([1, 25, 20, 10, 0, 15])
            pref_qwo = np.array([0, 0, 0, 4, 40, 0])
            self.rank = [p for p in determine_sets(pref, pref_qwo, self.decision_matrix, directions)[:3, :]]

        t2 = time.time()
        self.ids["time"].text = f"Czas: {int((t2 - t1) * 1000)} [ms]"
        rank_places: List[str] = []

        for i, alternative in enumerate(self.rank):
            for title, row in self.decision_matrix_df.iterrows():
                row_value = np.array([row["writer"], row["present_cast"], row["cast_popularity"], row["rating"],
                                      row["release_year_diff"], row["special_effects"]])
                if (row_value == alternative).all():
                    rank_places.append(f"{i + 1}. {title}")

        self.ids["rank"].text = "\n".join(rank_places)

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
