from random import randint
from typing import List, Union, Optional
from numpy import sqrt
from pandas import read_excel, DataFrame


def lesser_or_equal(point1: List[float], point2: List[float]) -> bool:
    n: int = len(point1)
    comparison: List[Optional[bool]] = [None for _ in range(n)]
    for i in range(n):
        comparison[i] = point1[i] <= point2[i]
    if sum(comparison) == n:
        return True
    else:
        return False


def algorytm_z_filtracja(base_X: List[List[float]]) -> List[List[float]]:
    """
    Algorytm odfiltrowuje punkty niezdominowane - uwaga, działą tylko dla minimalizacji
    :param base_X: bazowy zbiór punktów
    :return: zbiór punktów niezdominowanych, liczba porównań punktów oraz czas wykonania się algorytmu
    """
    X: List[List[float]] = [el for el in base_X]
    inf: int = max([sum(el) for el in X])
    inf_point: List[float] = [inf for _ in range(len(X[0]))]
    P: List[List[float]] = []
    n: int = len(X)
    for i in range(n):
        if X[i] == inf_point:
            continue
        Y: List[float] = X[i]
        for j in range(i + 1, n):
            if lesser_or_equal(Y, X[j]):
                X[j] = inf_point
            elif lesser_or_equal(X[j], Y):
                X[X.index(Y)] = inf_point
                Y = X[j]
        P.append(Y)
        for point in X:
            if lesser_or_equal(Y, point):
                X[X.index(point)] = inf_point
        if len(X) == 1:
            P.append(X[0])
            break
        if i + 1 > n:
            break
    return P


def metoda_zbiorow_odniesienia(daneA: List[List[Union[float, str]]], zbiorA0: List[List[Union[float, str]]],
                               zbiorA1: List[List[Union[float, str]]], zbiorA2: List[List[Union[float, str]]],
                               zbiorA3: List[List[Union[float, str]]], wektorWag: Optional[List[float]] = None,
                               normaCzebyszewa: bool = False) -> List[List[float]]:
    """
    Funkcja zwracająca ranking optymalnych punktów z danego zbioru
    :param zbiorA0: zbiór punktów granicznie optymalnych
    :param zbiorA3: zbiór punktów anty-idealnych
    :param zbiorA2: zbiór punktów status quo
    :param zbiorA1: zbiór modelów
    :param daneA: Wczytane z Excela dane (włącznie z etykietami) - należy ustawić zmienne offset na odpowiednie liczby
    tak, by ominąć etykiety wczytując dane (informacja czy kryterium jest minimalizowane, czy maksymalizowane, powinna
    być umieszczona w drugim wierszu od góry)
    :param wektorWag: można samemu podać wektor wag
    :param normaCzebyszewa: czy zostanie użyta norma Czebyszewa
    :return: Lista punktów optymalnych
    """
    # Wielkość problemu
    # Wartości "offsetXX" to ilości kolumn/wierszy do pominięcia, zawierające napisy, a nie liczby, w arkuszu
    offsetAl: int = 2
    offsetKr: int = 1
    liczbaAlternatyw: int = len(daneA) - offsetAl
    liczbaKryteriow: int = len(daneA[0]) - offsetKr
    # Ilość punktów odpowiednich klas
    offsetPKl: int = 1  # offset dla ilości punktów w zbiorach A0, 1, 2, 3
    liczbaA0: int = len(zbiorA0) - offsetPKl
    liczbaA1: int = len(zbiorA1) - offsetPKl
    liczbaA2: int = len(zbiorA2) - offsetPKl
    liczbaA3: int = len(zbiorA3) - offsetPKl
    # Sprawdzenie czy dane kryterium ma być minimalizowane, czy maksymalizowane
    cel: List[str] = daneA[0][offsetKr:]
    # Środki ciężkości zbiorów A0, A1, A2, A3
    center_A0: List[float] = [sum([zbiorA0[i][j] for i in range(offsetPKl, liczbaA0 + offsetPKl)]) / liczbaA0 for j in
                              range(offsetKr, liczbaKryteriow + offsetPKl)]
    center_A1: List[float] = [sum([zbiorA1[i][j] for i in range(offsetPKl, liczbaA1 + offsetPKl)]) / liczbaA1 for j in
                              range(offsetKr, liczbaKryteriow + offsetPKl)]
    center_A2: List[float] = [sum([zbiorA2[i][j] for i in range(offsetPKl, liczbaA2 + offsetPKl)]) / liczbaA2 for j in
                              range(offsetKr, liczbaKryteriow + offsetPKl)]
    center_A3: List[float] = [sum([zbiorA3[i][j] for i in range(offsetPKl, liczbaA3 + offsetPKl)]) / liczbaA3 for j in
                              range(offsetKr, liczbaKryteriow + offsetPKl)]
    # Sprawdzenie punktów alternatyw - czy mieszczą się między środkiem ciężkości granic optymalności oraz punktów
    # antyidealnych
    alternatywyOK: List[int] = [0 for _ in range(liczbaAlternatyw)]
    liczbaAlternatywTemp: int = 0  # Liczba alternatyw mieszczących się między punktami odniesienia
    for i in range(offsetAl, liczbaAlternatyw + offsetAl):
        for j in range(offsetKr, liczbaKryteriow + offsetKr):
            if center_A3[j - offsetKr] <= daneA[i][j] <= center_A0[j - offsetKr]:
                alternatywyOK[i - offsetAl] = i - offsetAl + 1
                liczbaAlternatywTemp += 1
            else:
                alternatywyOK[i - offsetAl] = 0
    # Uzupełnienie macierzy decyzyjnej
    id_in_matrix: int = 0
    macierz_decyzyjna: List[List[float]] = [[0 for _ in range(liczbaKryteriow)] for _ in
                                            range(liczbaAlternatywTemp)]
    for i in range(offsetAl, liczbaAlternatyw + offsetAl):
        if alternatywyOK[i - offsetAl] != 0:
            for j in range(offsetKr, liczbaKryteriow + offsetKr):
                macierz_decyzyjna[id_in_matrix][j - offsetKr] = daneA[i][j]
            id_in_matrix += 1
    # Usunięcie punktów zdominowanych
    # Z racji tego, że algorytm filtrujący działa tylko dla minimalizacji, należy zmienić wartości w kolumnach
    # odpowiadających maksymalizowanym kryteriom na przeciwne
    macierz_decyzyjna = algorytm_z_filtracja([[wiersz[j] if cel[j] == "min" else - wiersz[j] for j in
                                               range(liczbaKryteriow)] for wiersz in macierz_decyzyjna])
    # Po wyjściu z funkcji wartości muszą ponownie zostać zmienione na przeciwne w odpowiednich kolumnach
    macierz_decyzyjna = [[wiersz[j] if cel[j] == "min" else - wiersz[j] for j in range(liczbaKryteriow)]
                         for wiersz in macierz_decyzyjna]
    liczbaAlternatyw = len(macierz_decyzyjna)
    # Uzupełnienie wektora z wagami, jeśli nie został podany
    if wektorWag is None:
        wektorWag = [randint(1, 9) / 10 for _ in range(liczbaKryteriow)]
    # Normalizacja wag
    wektorWag = [elem / sum(wektorWag) for elem in wektorWag]
    # Skalowanie
    macierz_skalowania: List[List[float]] = [[0 for _ in range(liczbaKryteriow)] for _ in
                                             range(liczbaAlternatyw)]
    for i in range(liczbaAlternatyw):
        for j in range(liczbaKryteriow):
            if normaCzebyszewa:
                macierz_skalowania[i][j] = (macierz_decyzyjna[i][j] * wektorWag[j]) / max([abs(wiersz[j]) for wiersz
                                                                                           in macierz_decyzyjna])
            else:
                macierz_skalowania[i][j] = (macierz_decyzyjna[i][j] * wektorWag[j]) / \
                                           sqrt(sum([wiersz[j] ** 2 for wiersz in macierz_decyzyjna]))
    # Wyznaczenie odleglosci w przestrzeni euklidesowej
    odleglosci: List[List[float]] = [[0, 0] for _ in range(liczbaAlternatyw)]
    for i in range(liczbaAlternatyw):
        suma_idealny: float = 0
        suma_antyidealny: float = 0
        for j in range(liczbaKryteriow):
            suma_idealny += (macierz_skalowania[i][j] - center_A1[j]) ** 2
            suma_antyidealny += (macierz_skalowania[i][j] - center_A2[j]) ** 2
        odleglosci[i][0] = sqrt(suma_idealny)
        odleglosci[i][1] = sqrt(suma_antyidealny)
    # Uszeregowanie obiektów
    ranking: List[List[Union[int, float]]] = [[0, 0] for _ in range(liczbaAlternatyw)]
    for i in range(liczbaAlternatyw):
        ranking[i][0] = i
        ranking[i][1] = odleglosci[i][1] / (odleglosci[i][0] + odleglosci[i][1])
    ranking.sort(key=lambda x: x[1], reverse=True)
    posortowane_punkty: List[List[float]] = [[] for _ in range(liczbaAlternatyw)]
    for i in range(liczbaAlternatyw):
        posortowane_punkty[i] = macierz_decyzyjna[ranking[i][0]]
    return posortowane_punkty


def main_function(filename: str, wektor_wag: List[float], normaCzebyszewa: bool = False):
    sheets = read_excel(filename, sheet_name=None)
    arkusz_dane: DataFrame = sheets['Dane']
    arkusz_zbiorA0: DataFrame = sheets['A0']
    arkusz_zbiorA1: DataFrame = sheets['A1']
    arkusz_zbiorA2: DataFrame = sheets['A2']
    arkusz_zbiorA3: DataFrame = sheets['A3']
    dane: List[List[Union[float, str]]] = arkusz_dane.values.tolist()
    zbiorA0: List[List[Union[float, str]]] = arkusz_zbiorA0.values.tolist()
    zbiorA1: List[List[Union[float, str]]] = arkusz_zbiorA1.values.tolist()
    zbiorA2: List[List[Union[float, str]]] = arkusz_zbiorA2.values.tolist()
    zbiorA3: List[List[Union[float, str]]] = arkusz_zbiorA3.values.tolist()
    wynik: List[List[Union[float, str]]] = metoda_zbiorow_odniesienia(dane, zbiorA0, zbiorA1, zbiorA2, zbiorA3,
                                                                      wektor_wag, normaCzebyszewa)
    first_row: List[str] = [f"F{i}" for i in range(1, len(wektor_wag) + 1)]
    wynik.insert(0, first_row)
    df: DataFrame = DataFrame(wynik)
    df.to_excel("zbiory_odniesienia-wyniki.xlsx", "Wyniki - posortowane punkty")
    print("Posortowane punkty:")
    print(df)


if __name__ == '__main__':
    # Należy podać nazwę pliku oraz wektor wag o długości równej ilości kryteriów, a także opcjonalnie podać czy chce
    # się użyć normy Czebyszewa
    main_function("Dane.xlsx", [1, 1])
