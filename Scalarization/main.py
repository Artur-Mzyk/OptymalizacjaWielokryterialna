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

    for _ in range(100):
        # radius = np.random.rand()
        radius = 1
        theta = np.random.rand() * 2 * np.pi
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        D.append((x, y))

    D = np.array(D)

    x = np.array([v[0] for v in D])
    y = np.array([v[1] for v in D])
    ideal_point = [min(f1(x, y)), min(f2(x, y))]

    plt.figure()
    plt.scatter(x, y)
    plt.xlabel("x"), plt.ylabel("y")
    plt.show()

    plt.figure()
    plt.scatter(f1(x, y), f2(x, y))
    plt.xlabel("F1"), plt.ylabel("F2")
    plt.show()


    # plt.scatter(f1(x, y), f2(x, y))
    # plt.xlabel("F1"), plt.ylabel("F2")
    # plt.show()
    print(D)
    print(ideal_point)

