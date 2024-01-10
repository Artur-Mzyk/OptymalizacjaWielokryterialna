#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from imdb import IMDb, Cinemagoer, IMDbBase
from imdb import Movie
from bs4 import BeautifulSoup
from typing import List, Dict
from imdb.parser.http import IMDbHTTPAccessSystem
import time
from concurrent.futures import ThreadPoolExecutor


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
        movies: List[Movie.Movie] = [self.imdb.get_movie(item['titleId'][2:], info=["main"]) for item in items]

        return movies

    def get_genres(self) -> List[str]:
        url: str = "https://www.imdb.com/feature/genre/"
        print(f"[DOWNLOAD] From {url}")
        content = self.imdb._retrieve(url)
        soup = BeautifulSoup(content, 'html.parser')
        response = json.loads(soup.find('script', {"id" : "__NEXT_DATA__"}).text)
        genres = [genre["displayText"] for genre in response["props"]["pageProps"]["movieGenreList"]]

        return genres

    def get_cast_popularity(self, code: str) -> int:
        filmography = self.imdb.get_person_filmography(code)['data']['filmography']

        if "actor" in filmography:
            return len(filmography["actor"])

        else:
            return 0


if __name__ == '__main__':
    query = Query()
    genre = "fantasy"
    n_movies = 10

    # movies = query.get_top_movies(genre, n_movies)

    # for movie in movies:
    #     print(movie)

    t1 = time.time()
    imdb: IMDbHTTPAccessSystem = IMDb()

    criteria = {'genres': genre, 'count': str(n_movies), 'sort': "num_votes,desc"}
    params = '&'.join([f"{k}={v}" for k, v in criteria.items()])
    url = imdb.urls['search_movie_advanced'] % params

    # Pobranie danych
    print(f"[DOWNLOAD] From {url}")
    content = imdb._retrieve(url)

    # Parsowanie danych
    soup = BeautifulSoup(content, 'html.parser')
    response = json.loads(soup.find('script', {"id" : "__NEXT_DATA__"}).text)
    items = response['props']['pageProps']['searchResults']['titleResults']['titleListItems']

    for item in items:
        # movie = imdb.get_movie(item['titleId'][2:], info=["main"])
        t2 = time.time()
        print(f"Czas: {int((t2 - t1) * 1000)} [ms]")
