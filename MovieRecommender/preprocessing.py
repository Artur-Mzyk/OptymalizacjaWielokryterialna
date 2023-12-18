#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from imdb import IMDb, Cinemagoer, IMDbBase
from imdb import Movie
from bs4 import BeautifulSoup
from typing import List, Dict


def get_top_movies(genre: str, n_movies: int) -> Dict[str, str]:

    # Stworzenie obiektu klasy IMDb
    imdb = IMDb()

    # Konkatenacja URL potrzebnego do pobrania danych
    criteria = {'genres': genre, 'count': str(n_movies), 'sort': "num_votes,desc"}
    params = '&'.join(['%s=%s' % (k, v) for k, v in criteria.items()])
    url = imdb.urls['search_movie_advanced'] % params

    # Pobranie danych
    content = imdb._retrieve(url)

    # Parsowanie danych
    soup = BeautifulSoup(content, 'html.parser')
    response = json.loads(soup.find('script', {"id" : "__NEXT_DATA__"}).text)
    movies: Dict[str, str] = {}

    for i in range(n_movies):
        item = response['props']['pageProps']['searchResults']['titleResults']['titleListItems'][i]
        movies[item['titleId'][2:]] = item['titleText']

    return movies


if __name__ == '__main__':
    ia = IMDb()
    genre = "fantasy"
    n_movies = 8
    movies = get_top_movies(genre, n_movies)
    print(movies)
    movies_list = [Movie.Movie(movieID=ia._get_real_movieID(mi), data=md, modFunct=ia._defModFunct,
                               accessSystem=ia.accessSystem) for mi, md in movies.items()]
