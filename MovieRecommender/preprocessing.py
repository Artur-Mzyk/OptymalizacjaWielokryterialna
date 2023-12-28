#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from imdb import IMDb, Cinemagoer, IMDbBase
from imdb import Movie
from bs4 import BeautifulSoup
from typing import List, Dict
from imdb.parser.http import IMDbHTTPAccessSystem


class Query:
    def __init__(self) -> None:

        # Stworzenie obiektu klasy IMDb
        self.imdb: IMDbHTTPAccessSystem = IMDb()

    def get_top_movies(self, genre: str, n_movies: int) -> List[Movie.Movie]:

        # Konkatenacja URL potrzebnego do pobrania danych
        criteria = {'genres': genre, 'count': str(n_movies), 'sort': "num_votes,desc"}
        params = '&'.join([f"{k}={v}" for k, v in criteria.items()])
        url = self.imdb.urls['search_movie_advanced'] % params

        # Pobranie danych
        print(f"[DOWNLOAD] From {url}")
        content = self.imdb._retrieve(url)

        # Parsowanie danych
        soup = BeautifulSoup(content, 'html.parser')
        response = json.loads(soup.find('script', {"id" : "__NEXT_DATA__"}).text)
        items = response['props']['pageProps']['searchResults']['titleResults']['titleListItems']
        movies: List[Movie.Movie] = [self.imdb.get_movie(item['titleId'][2:]) for item in items]

        return movies

    def get_genres(self) -> List[str]:
        url: str = "https://www.imdb.com/feature/genre/"
        print(f"[DOWNLOAD] From {url}")
        content = self.imdb._retrieve(url)
        soup = BeautifulSoup(content, 'html.parser')
        response = json.loads(soup.find('script', {"id" : "__NEXT_DATA__"}).text)
        genres = [genre["displayText"] for genre in response["props"]["pageProps"]["movieGenreList"]]

        return genres


if __name__ == '__main__':
    query = Query()
    genre = "fantasy"
    n_movies = 5

    # TODO Dorobić obsługę obrony przed duplikowaniem się filmów
    movies = query.get_top_movies(genre, n_movies)

    for movie in movies:
        print(movie)
