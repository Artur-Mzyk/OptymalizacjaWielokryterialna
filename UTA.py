#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


# Funkcja do znajdowania min i max dla każdego kryterium (iteracja po kolumnach)
def find_minmax_criteria(A):
    min_gi = [min(A[:, i]) for i in range(len(A[0]))]
    max_gi = [max(A[:, i]) for i in range(len(A[0]))]
    return min_gi, max_gi


# Funkcja do obliczania cząstkowych użyteczności (przy założeniu że funkcje są liniowe)
def calc_u(A, min_gi, max_gi, minmax, criteria=[], weights=[]):
    U = np.zeros(A.shape)
    for k in range(A.shape[1]):
        if minmax[k]:
            for a in range(A.shape[0]):
                U[a, k] = ((A[a, k]-min_gi[k]) / (max_gi[k]-min_gi[k])) * weights[k]
        else:
            for a in range(A.shape[0]):
                U[a, k] = (1-((A[a, k]-min_gi[k]) / (max_gi[k]-min_gi[k]))) * weights[k]
    return U


# Sumowanie użyteczności dla każdego wariantu
def calc_utilities_for_a(U):
    utilities = {}
    for i in range(len(U)):
        utilities[i] = round(sum(U[i]), 5)
    return utilities


# Sortowanie użyteczności i przypisywanie wariantów
def sort_a(utilities):
    usort = dict(sorted(utilities.items(), key=lambda item: item[1], reverse=True))
    return np.array(usort.keys())


# Wywołanie powyższych funkcji jako użycie metody UTA (zwraca ranking)
def UTASTAR(A, minmax, criteria=[], weights=[]): 
    if not weights:
        weights = [1 / len(minmax) for i in range(len(minmax))]
    if not criteria:
        criteria = [i + 1 for i in range(len(minmax))]

    min_g, max_g = find_minmax_criteria(A)
    U = calc_u(A, min_g, max_g, minmax, criteria, weights)
    util = calc_utilities_for_a(U)
    rank = sort_a(util)
    return rank
