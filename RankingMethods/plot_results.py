#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_results(all_points, dominated, nondominated):

    # Rozpakowanie danych
    x_all, y_all, z_all, color_all = zip(*all_points)
    x_nondominated, y_nondominated, z_nondominated, color_nondominated = zip(*nondominated)
    x_dominated, y_dominated, z_dominated, color_dominated = zip(*dominated)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Wykres punktów niezdominowanych
    ax.scatter(x_nondominated, y_nondominated, z_nondominated, marker='D', label='Niezdominowane', s=80, edgecolor='blue', facecolor='white')

    # Wykres punktów zdominowanych
    ax.scatter(x_dominated, y_dominated, z_dominated, marker='o', label='Zdominowane', s=80, edgecolor='red', facecolor='white')

    # Wykres wszystkich punktów
    all_scatter = ax.scatter(x_all, y_all, z_all, c=color_all, marker ="*", label="Zbiór punktów", cmap='jet', s=40, linewidths=2)

    ax.set_xlabel('Kryterium 1')
    ax.set_ylabel('Kryterium 2')
    ax.set_zlabel('Kryterium 3')

    # Dodanie colorbaru
    cbar = plt.colorbar(all_scatter, label='Kryterium 4', location = 'left')
    cbar.set_ticks([min(color_all), max(color_all)])

    plt.legend()
    plt.title('Wykres 3D z punktami niezdominowanymi i zdominowanymi')
    plt.show()
