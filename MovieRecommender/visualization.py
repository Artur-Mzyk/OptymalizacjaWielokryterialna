#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def plot_results(all_points, rank_points) -> None:
    if not all_points:
        return None

    fig = plt.figure()

    if len(all_points[0]) == 3:
        x_all, y_all, z_all = zip(*all_points)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x_all, y_all, z_all, marker ="*", label="Zbiór alternatyw")

        if len(rank_points) >= 1:
            rank1 = rank_points[0]
            ax.scatter([rank1[0]], [rank1[1]], [rank1[2]], c="red", marker ="o", label="Ranking 1")

        if len(rank_points) >= 2:
            rank2 = rank_points[1]
            ax.scatter([rank2[0]], [rank2[1]], [rank2[2]], c="green", marker ="o", label="Ranking 2")

        if len(rank_points) >= 3:
            rank3 = rank_points[2]
            ax.scatter([rank3[0]], [rank3[1]], [rank3[2]], c="black", marker ="o", label="Ranking 3")

        ax.set_zlabel('Rok produkcji')

    elif len(all_points[0]) == 2:
        x_all, y_all = zip(*all_points)
        ax = fig.add_subplot(111)
        ax.scatter(x_all, y_all, c="blue", marker ="*", label="Zbiór alternatyw")

        if len(rank_points) >= 1:
            rank1 = rank_points[0]
            ax.scatter([rank1[0]], [rank1[1]], c="red", marker ="o", label="Ranking 1")

        if len(rank_points) >= 2:
            rank2 = rank_points[1]
            ax.scatter([rank2[0]], [rank2[1]], c="green", marker ="o", label="Ranking 2")

        if len(rank_points) >= 3:
            rank3 = rank_points[2]
            ax.scatter([rank3[0]], [rank3[1]], c="black", marker ="o", label="Ranking 3")

    elif len(all_points[0]) == 6:
        x1_all, x2_all, x3_all, x4_all, x5_all, x6_all = zip(*all_points)
        n = len(x1_all)
        indx_lst = [i + 1 for i in range(n)]
        rank1 = rank_points[0]
        rank1 = rank1.tolist()
        rank1_indx = all_points.index(rank1) + 1

        rank1_lst = [rank1[0] for _ in range(n)]
        ax = fig.add_subplot(231)
        ax.scatter(indx_lst, x1_all, c="blue", marker="*")
        ax.scatter(rank1_indx, rank1[0], c="red", marker="o")
        ax.set_title("Autor")

        rank2_lst = [rank1[1] for _ in range(n)]
        ax = fig.add_subplot(232)
        ax.scatter(indx_lst, x2_all, c="blue", marker="*")
        ax.scatter(rank1_indx, rank1[1], c="red", marker="o")
        ax.set_title("Obsada")

        rank3_lst = [rank1[2] for _ in range(n)]
        ax = fig.add_subplot(233)
        ax.scatter(indx_lst, x3_all, c="blue", marker="*")
        ax.scatter(rank1_indx, rank1[2], c="red", marker="o")
        ax.set_title("Popularnosc obsady")

        rank4_lst = [rank1[3] for _ in range(n)]
        ax = fig.add_subplot(234)
        ax.scatter(indx_lst, x4_all, c="blue", marker="*")
        ax.scatter(rank1_indx, rank1[3], c="red", marker="o")
        ax.set_title("Ocena")

        rank5_lst = [rank1[4] for _ in range(n)]
        ax = fig.add_subplot(235)
        ax.scatter(indx_lst, x5_all, c="blue", marker="*")
        ax.scatter(rank1_indx, rank1[4], c="red", marker="o")
        ax.set_title("Rok produkcji")

        rank6_lst = [rank1[5] for _ in range(n)]
        ax = fig.add_subplot(236)
        ax.scatter(indx_lst, x6_all, c="blue", marker="*")
        ax.scatter(rank1_indx, rank1[5], c="red", marker="o")
        ax.set_title("Efekty specjalne")


    # ax.set_xlabel('Obsada')
    # ax.set_ylabel('Ocena')
    # plt.legend()

    return fig
