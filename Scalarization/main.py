import numpy as np
import matplotlib.pyplot as plt


f1 = lambda x, y: x - y**2 + 1
f2 = lambda x, y: x**2 - y**2 + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # mean = 5
    # std = 1
    # number_of_points = 20
    # number_of_parameters = 2
    # D = np.random.normal(mean, std, (number_of_points, number_of_parameters))

    D = []
    N = 1000

    for _ in range(N):
        r, theta = 1, np.random.rand() * 2 * np.pi
        D.append((r * np.cos(theta), r * np.sin(theta)))

    D = np.array(D)

    x = np.array([v[0] for v in D])
    y = np.array([v[1] for v in D])
    F1 = f1(x, y)
    F2 = f2(x, y)
    ideal_x, ideal_y = min(F1), min(F2)

    S = [(F1[i] - ideal_x)**2 + (F2[i] - ideal_y)**2 for i in range(N)]
    idx = S.index(min(S))

    fig, ax = plt.subplots(nrows=1, ncols=2)
    ax[0].scatter(x, y)
    ax[0].scatter([x[idx]], [y[idx]])
    ax[0].set_xlabel("x"), ax[0].set_ylabel("y")

    ax[1].scatter(F1, F2)
    ax[1].scatter([ideal_x], [ideal_y])
    ax[1].scatter([F1[idx]], [F2[idx]])
    ax[1].set_xlabel("F1"), ax[1].set_ylabel("F2")
    plt.show()

