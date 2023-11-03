from typing import List

# Algorithm 1

def algorithm_1(X):
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


def algorithm_2(X):
    X_list = X.copy()
    P = []
    deleted = list()
    i = 0
    while i < len(X_list):
        was_removed = False
        Y = X_list[i]
        j = i + 1
        while j < len(X_list):
            min_val = get_minimum(Y, X_list[j])
            if min_val == Y:
                if X_list[j] not in deleted: deleted.append(X_list[j])
                X_list.remove(X_list[j])
                was_removed = True
            elif min_val == X_list[j]:
                Y_temp = Y
                Y = X_list[j]
                X_list.remove(Y_temp)
                was_removed = True
            else:
                j += 1
        P.append(Y)
        k = 0
        while k < len(X_list):
            min_val = get_minimum(Y, X_list[k])
            if min_val == Y:
                X_list.remove(X_list[k])
                was_removed = True
            else:
                k += 1
        if len(X_list) == 1:
            P.append(X_list[0])
            return P
        if not was_removed:
            i += 1
    return P


# Algorithm 3

# class Point:
#   def __init__(self, coords: List[float]) -> None:
#     self.coords = coords
#     self.n = len(coords)

#   def __le__(self, other: "Point") -> bool:
#     for i in range(self.n):
#       if self.coords[i] > other.coords[i]:
#         return False

#     return True

#   def __str__(self) -> str:
#     return "(" + ", ".join([str(x) for x in self.coords]) + ")"

#   def print(self) -> str:
#     print(self)

#   def dist(self, other: "Point") -> float:
#     d: float = 0

#     for i in range(self.n):
#       d += (self.coords[i] - other.coords[i])**2

#     return d

def algorithm_3(X):
  X_list = X.copy()
  P = list()
  k = len(X_list[0])
  ideal_point_coords: List[float] = []

  for i in range(k):
    ideal_point_coords.append(min([x[i] for x in X_list]))

  ideal_point = ideal_point_coords

  n: int = len(X_list)
  sorted_points: List[float] = []

  for j in range(n):
    d: float = sum((ideal_point[i] - X[j][i]) ** 2 for i in range(k))
    sorted_points.append((d, j))

  sorted_points = sorted(sorted_points, key=lambda v: v[0])
  D = [elem[0] for elem in sorted_points]
  J = [elem[1] for elem in sorted_points]
  M: int = n
  m: int = 0

  while m <= M:
    if X_list[J[m]] is None:
      m += 1
      continue

    for i in range(n):
      if X_list[i] is None or J[m] == i:
        continue

      if all(X_list[J[m]][j] <= X_list[i][j] for j in range(k)):
        X_list[i] = None

    P.append(X_list[J[m]])
    X_list[J[m]] = None
    M = M - 1
    m = m + 1

  return P

if __name__ == "__main__":
    X = [(5,5), (3,6), (4,4), (5,3), (3,3), (1,8), (3,4), (4,5), (3,10), (6,6), (4,1), (3,5)]
    P1, dominated1 = algorithm_1(X)
    print("Algorytm 1: \n {}".format(P1))
    P2 = algorithm_2(X)
    print("Algorytm 2: \n {}".format(P2))
    P3 = algorithm_3(X)
    print("Algorytm 3: \n {}".format(P3))




