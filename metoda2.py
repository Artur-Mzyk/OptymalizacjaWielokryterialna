from typing import List

def get_minimum(x1, x2):
    min_x1 = [0 if x1[i] <= x2[i] else 1 for i in range(len(x1))]
    min_x2 = [0 if x2[i] <= x1[i] else 1 for i in range(len(x2))]
    if max(min_x1) == 0:
        return x1
    elif max(min_x2) == 0:
        return x2
    else:
        return None


def alg2(X):
    P = []
    dominated_points = []
    i = 0
    while i < len(X):
        was_removed = False
        Y = X[i]
        j = i + 1
        while j < len(X):
            min_val = get_minimum(Y, X[j])
            if min_val == Y:
                dominated_points.append(X[j])
                X.remove(X[j])
                was_removed = True
            elif min_val == X[j]:
                Y_temp = Y
                Y = X[j]
                dominated_points.append(Y_temp)
                X.remove(Y_temp)
                was_removed = True
            else:
                j += 1
        P.append(Y)
        k = 0
        X.remove(Y)
        while k < len(X):
            min_val = get_minimum(Y, X[k])
            if min_val == Y:
                dominated_points.append(X[k])
                X.remove(X[k])
                was_removed = True
            else:
                k += 1
        if len(X) == 1:
            P.append(X[0])
            return P, dominated_points
        if not was_removed:
            i += 1
    return P, dominated_points

if __name__ == '__main__':
    X = [[5, 5], [3, 6], [4, 4], [5, 3], [3, 3], [1, 8], [3, 4], [4, 5], [3, 10], [6, 6], [4, 1], [3, 5]]
    P, dom_points = alg2(X)
    print(P)
    print(dom_points)