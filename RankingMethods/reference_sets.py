import numpy as np
import pandas as pd

from copy import deepcopy


# Wyznaczenie decyzji między zbiorem A1 i A2 do stworzenia rankingu (jeżeli pomiędzy jest zbiór pusty to rozważamy zbiór A2)
def wyznaczanie_zbioru_mozliwych_decyzji(A1, A2, D):
    liczba_kryteriów = D.shape[1] - 1
    liczba_decyzji = D.shape[0]

    liczba_alternatyw_A1 = A1.shape[0]
    liczba_alternatyw_A2 = A2.shape[0]

    M1 = []
    for i in range(liczba_decyzji):
        warunek = False
        for a in range(liczba_alternatyw_A1):
            for j in range(1, liczba_kryteriów + 1):
                if D[i,j] >= A1[a,j]:
                    warunek = True
                else:
                    warunek = False
                    break
        if warunek:
            wpisuj = True
            for k in range(liczba_alternatyw_A1):
                if np.equal(A1[k,:], D[i,:]).all():
                    wpisuj = False
                    break
            if wpisuj:
                M1.append(D[i,:])
    M1 = np.array(M1)
    liczba_alt_M1 = M1.shape[0]

    M2 = []
    for i in range(liczba_alt_M1):
        warunek = False
        for a in range(liczba_alternatyw_A2):
            for j in range(1, liczba_kryteriów + 1):
                if M1[i,j] <= A2[a,j]:
                    warunek = True
                else:
                    warunek = False
                    break
        if warunek:
            wpisuj = True
            for k in range(liczba_alternatyw_A2):
                if np.equal(A2[k,:], M1[i,:]).all():
                    wpisuj = False
                    break
            if wpisuj:
                M2.append(M1[i,:])

    if M2 == []:
        M2 = A2
    else:
        M2 = np.array(M2)
    return M2




def reverse_max_criteria(D, directions):
    n_criteria = len(directions)

    for i in range(n_criteria):
        if directions[i] == 'max':
            D[:, i + 1] = -D[:, i + 1]

    return D


def punkty_niezdominowe_nieporownywalne(D):
    n_alternatives = D.shape[0]
    n_criteria = D.shape[1] - 1

    incomparable_points = D[0, :].reshape((1, n_criteria + 1))
    non_dominated_point = D[0, :]

    for i in range(1, n_alternatives):
        n_greater = 0
        n_equal = 0

        for j in range(1, n_criteria + 1):
            if non_dominated_point[j] < D[i, j]:
                n_greater += 1

            elif non_dominated_point[j] == D[i, j]:
                n_equal += 1

        r = n_criteria - n_equal

        if  r == 0 or 0 < n_greater < r:
            incomparable_points = np.concatenate((incomparable_points, D[i, :].reshape((1, n_criteria + 1))), axis=0)

        elif n_greater == 0:
            incomparable_points_old = incomparable_points
            non_dominated_point = D[i, :]

            # Porównanie czy nowy punkt dominuje nad starymi w macierzy nieporównywalne:
            if incomparable_points_old.shape[0] != 1:
                incomparable_points_old = np.concatenate((non_dominated_point.reshape((1,n_criteria + 1)), incomparable_points_old), axis=0)
                incomparable_points = punkty_niezdominowe_nieporownywalne(incomparable_points_old)

            else:
                incomparable_points = non_dominated_point.reshape((1, n_criteria + 1))

    return incomparable_points


def best_points(D, direction):
    n_criteria = D.shape[1] - 1

    if direction == 'max':
        D[:, 1:n_criteria + 1] = -D[:, 1:n_criteria + 1]

    incomparable_points_part = punkty_niezdominowe_nieporownywalne(D)
    non_dominated_point = incomparable_points_part[0, :]
    incomparable_points = non_dominated_point.reshape((1, n_criteria + 1))

    while incomparable_points_part.shape[0] > 2:
        incomparable_points_part = punkty_niezdominowe_nieporownywalne(incomparable_points_part[1:, :])
        non_dominated_point = incomparable_points_part[0, :]
        incomparable_points = np.concatenate((non_dominated_point.reshape((1, n_criteria + 1)), incomparable_points), axis=0)

    if incomparable_points_part.shape[0] == 2:
        incomparable_points = np.concatenate((incomparable_points_part[1, :].reshape((1, n_criteria + 1)), incomparable_points), axis=0)

    A0 = incomparable_points
    idealny = np.array([[A0[:, i].min() for i in range(1, A0.shape[1])]])

    if direction == 'max':
        A0[:, 1:A0.shape[1]] = -A0[:, 1:A0.shape[1]]
        idealny = -idealny

    if direction == 'max':
        D[:, 1:D.shape[1]] = -D[:, 1:D.shape[1]]

    return A0, idealny


def nieporownywalne_dla_preferencji(pref, D):
    n_alternatives = D.shape[0]
    n_criteria = D.shape[1] - 1
    incomparable_points = np.array([])

    for i in range(1, n_alternatives):
        n_greater = 0
        n_equal = 0

        for j in range(1, n_criteria + 1):
            if pref[j - 1] < D[i, j]:
                n_greater += 1

            elif pref[j - 1] == D[i, j]:
                n_equal += 1

        r = n_criteria - n_equal

        if r == 0 or 0 < n_greater < r:
            if incomparable_points.shape[0] == 0:
                incomparable_points = D[i, :].reshape((1, n_criteria + 1))

            incomparable_points = np.concatenate((incomparable_points, D[i, :].reshape((1, n_criteria + 1))), axis=0)

    return incomparable_points


def internal_contradiction(A):
    n_criteria = A.shape[1] - 1
    incomparable_points_part = punkty_niezdominowe_nieporownywalne(A)
    non_dominated_point = incomparable_points_part[0, :]
    incomparable_points = non_dominated_point.reshape((1, n_criteria + 1))

    while incomparable_points_part.shape[0] > 2:
        incomparable_points_part = punkty_niezdominowe_nieporownywalne(incomparable_points_part[1:, :])
        non_dominated_point = incomparable_points_part[0,:]
        incomparable_points = np.concatenate((non_dominated_point.reshape((1, n_criteria + 1)), incomparable_points), axis=0)

    if incomparable_points_part.shape[0] == 2:
        incomparable_points = np.concatenate((incomparable_points_part[1, :].reshape((1, n_criteria + 1)), incomparable_points), axis=0)

    return incomparable_points


def external_contradiction(A, B):
    n_criteria = A.shape[1] - 1
    n_alternatives_A = A.shape[0]
    n_alternatives_B = B.shape[0]
    new_alternatives_A = []

    for i in range(n_alternatives_A):
        condition = False
        comparison = 0

        for j in range(n_alternatives_B):
            for k in range(1, n_criteria + 1):
                if A[i, k] < B[j, k]:
                    condition = False
                    break

                else:
                    condition = True

            if condition:
                comparison = B[j, :]
                break

        if condition:
            if np.equal(A[i, :], comparison).all():
                pass

            else:
                new_alternatives_A.append(A[i, :])

    return np.array(new_alternatives_A)


def get_ideal_point(A, flag):
    if flag == 'max':
        A[:, 1:A.shape[1]] = -A[:, 1:A.shape[1]]

    ideal_point = np.array([[A[:, i].min() for i in range(1, A.shape[1])]])

    if flag == 'max':
        A[:, 1: A.shape[1]] = -A[:, 1: A.shape[1]]
        ideal_point = -ideal_point

    return ideal_point


def determine_sets(pref, pref_qwo):
    """
    :param pref: Preferencje do wyznaczenia zbioru A1 (nieosiągalnego dla klienta)
    :param pref_qwo: Preferencje minimalne do wyznaczenia zbioru A2 (klient chce coś więcej niż to)
    """

    criteria = ['Punkt', 'Marża [%]', 'Wkład własny [%]', 'Opinie[pkt. Max. 5]']
    directions = ['min', 'min', 'max']
    D = pd.read_excel("dane.xlsx", sheet_name='Arkusz3', header=0)[criteria].values
    D_min = reverse_max_criteria(D, directions)

    A0, vec_ideal = best_points(D_min, 'min')
    A3, vec_anty_ideal = best_points(D_min, 'max')

    A1 = nieporownywalne_dla_preferencji(pref, D_min)

    if A1.shape[0] == 0:
        A1 = deepcopy(A0)

    A1 = internal_contradiction(A1)
    A1 = external_contradiction(A1, A0)

    if A1.shape[0] == 0:
        A1 = deepcopy(A0)

    ideal_A1 = get_ideal_point(A1, 'min')

    A2 = nieporownywalne_dla_preferencji(pref_qwo, D_min)

    if A2.shape[0] == 0:
        A2 = deepcopy(A3)

    A2 = internal_contradiction(A2)
    A2 = external_contradiction(A2, A1)

    if A2.shape[0] == 0:
        A2 = deepcopy(A3)

    ideal_A2 = get_ideal_point(A2, 'max')

    M = wyznaczanie_zbioru_mozliwych_decyzji(A1, A2, D_min)

    if M.shape[0] == 0:
        M = deepcopy(A2)
        A2 = deepcopy(A3)

    # if 'max' in directions:
    #     M = reverse_max_criteria(M, directions)
    #     A0 = reverse_max_criteria(A0, directions)
    #     vec_ideal = reverse_max_criteria(vec_ideal, directions)
    #     vec_anty_ideal = reverse_max_criteria(vec_anty_ideal, directions)
    #     A3 = reverse_max_criteria(A3, directions)
    #     A2 = reverse_max_criteria(A2, directions)
    #     A1 = reverse_max_criteria(A1, directions)
    #     ideal_A1 = reverse_max_criteria(ideal_A1, directions)
    #     ideal_A2 = reverse_max_criteria(ideal_A2, directions)

    return A0, vec_ideal, A3, vec_anty_ideal, A1, ideal_A1, A2, ideal_A2, M, directions


if __name__ == "__main__":
    pref = np.array([1.2, 15, -5])
    pref_qwo = np.array([3.5, 42, -1])
    A0, vec_ideal, A3, vec_anty_ideal, A1, idealny_A1, A2, idealny_A2, M, flagi = determine_sets(pref, pref_qwo)

    print(f"Punkty najlepsze:\n{A0}\nWektor idealny:\t{vec_ideal}\n")
    print(f"Punkty najgorsze:\n{A3}\nWektor antyidealny:\t{vec_anty_ideal}\n")
    print(f"Punkty preferencji nieosiągalnych:\n{A1}\nWektor idealny z A1:\t{idealny_A1}\n")
    print(f"Punkty statu quo:\n{A2}\nWektor nadir z A2:\t{idealny_A2}\n")
    print(f"Pomiędzy A1 i A2:\t{M}")
