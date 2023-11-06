from typing import List
from plot_results import plot_results
from data_generation import generate_points_gamma
import math

# Algorithm 1

def algorithm_1(X, criteria):
    X_list = X.copy()
    not_dominated = list()
    not_comparable = list()
    deleted = list()
    n = len(X_list)
    for i in range(n):
        if X_list[i] is None:
            continue
        Y = X_list[i]
        fl = 0
        for j in range(i+1, n):
            if X_list[j] is None:
                continue
            if Y[0] <= X_list[j][0] and Y[1] <= X_list[j][1]:
                if X_list[j] not in deleted: deleted.append(X_list[j])
                X_list[j] = None
            elif Y[0] >= X_list[j][0] and Y[1] >= X_list[j][1]:
                id_ = X_list.index(Y)
                if X_list[id_] not in deleted: deleted.append(X_list[id_])
                X_list[id_] = None
                Y = X_list[j]
                fl = 1
            else:
                not_comparable.append(X_list[j])
                        
        if Y not in not_dominated: not_dominated.append(Y)
        if fl == 0:
            id_ = X_list.index(Y)
            X_list[id_] = None
        not_comparable = list()
    return not_dominated, deleted


# Algorithm 2

def get_minimum(x1, x2):
    min_x1 = [0 if x1[i] <= x2[i] else 1 for i in range(len(x1))]
    min_x2 = [0 if x2[i] <= x1[i] else 1 for i in range(len(x2))]
    if max(min_x1) == 0:
        return x1
    elif max(min_x2) == 0:
        return x2
    else:
        return None

def algorithm_2(X, criteria):
    X_list = X.copy()
    P = []
    dominated_points = []
    i = 0

    while i < len(X_list):
        was_removed = False
        Y = X_list[i]
        j = i + 1
        while j < len(X_list):
            min_val = get_minimum(Y, X_list[j])
            if min_val == Y:
                dominated_points.append(X_list[j])
                X_list.remove(X_list[j])
                was_removed = True
            elif min_val == X_list[j]:
                Y_temp = Y
                Y = X_list[j]
                dominated_points.append(Y_temp)
                X_list.remove(Y_temp)
                was_removed = True
            else:
                j += 1
        P.append(Y)
        k = 0
        X_list.remove(Y)
        while k < len(X_list):
            min_val = get_minimum(Y, X_list[k])
            if min_val == Y:
                dominated_points.append(X_list[k])
                X_list.remove(X_list[k])
                was_removed = True
            else:
                k += 1
        if len(X_list) == 1:
            P.append(X_list[0])
            return P, dominated_points
        if not was_removed:
            i += 1
    return P, dominated_points


# Algorithm 3
def algorithm_3(X, criteria):
    X_list = X.copy()
    dominated_points: List[List[float]] = []
    not_dominated_points: List[List[float]] = []
    k = len(X_list[0])
    n = len(X_list)
    ideal_point: List[float] = []

    for i in range(k):
        if criteria[i]:
            ideal_point.append(max([x[i] for x in X_list]))

        else:
            ideal_point.append(min([x[i] for x in X_list]))

    points_info: List[List[float]] = []

    for j in range(n):
        d = sum(abs(ideal_point[i] - X[j][i]) for i in range(k))
        points_info.append([d, j])

    sorted_points_info = sorted(points_info, key=lambda v: v[0])
    print(sorted_points_info)
    J = [elem[1] for elem in sorted_points_info]
    M, m = n, 0

    while m <= M:
        X_ref = X_list[J[m]]

        if X_ref is None:
            m += 1
            continue

        h = len([x for x in X_list if x is not None]) == 1

        for i in range(n):
            if X_list[i] is None or J[m] == i:
                continue

            for j in range(k):
                if criteria[j] and X_ref[j] < X_list[i][j]:
                    break

                elif not criteria[j] and X_ref[j] > X_list[i][j]:
                    break

            else:
                dominated_points.append(X_list[i])
                X_list[i] = None
                h = True

        if h:
            not_dominated_points.append(X_ref)

        else:
            dominated_points.append(X_ref)

        X_list[J[m]] = None
        M, m = M - 1, m + 1

    return not_dominated_points, dominated_points

if __name__ == "__main__":
    X = [(5, 5), (3, 6), (4, 4), (5, 3), (3, 3), (1, 8), (3, 4), (4, 5), (3, 10), (6, 6), (4, 1), (3, 5)]
    X = [(3, 4, -4, 5), (1, -4, -2, 1), (5, 5, -4, 5), (5, 0, 3, -4), (-1, 5, 3, 5), (2, -5, 4, 5)]
    input = generate_points_gamma(1, 4, 20, 4)

    # potrzebna konwersja, ponieważ wszystkie algorytmy działają na liście krotek jako zbiór punktów początkowych
    input = list(map(tuple, input))
    # input = X
    criteria = [False, True, True, False]

    P1, dominated1 = algorithm_1(input, criteria)
    P2, dominated2 = algorithm_2(input, criteria)
    P3, dominated3 = algorithm_3(input, criteria)
    print(f"Algorytm 1:\n\t{len(P1)}\t{P1}\n\t{len(dominated1)}\t{dominated1}")
    print(f"Algorytm 2:\n\t{len(P2)}\t{P2}\n\t{len(dominated2)}\t{dominated2}")
    print(f"Algorytm 3:\n\t{len(P3)}\t{P3}\n\t{len(dominated3)}\t{dominated3}")

    # plot_results(input, dominated1, P1)


