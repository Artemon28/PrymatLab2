from random import *
from numdifftools import Gradient
import numpy as np
import matplotlib.pyplot as plt
import FuncMinimization
import math


def steepest_descent_gradient(f, grad, x, eps, min_f, n=1000):
    steps = 0
    points = [np.copy(x)]
    for _ in range(n):
        steps += 1
        gr = grad(x)
        g = lambda l_: f(x - gr * l_)
        lam = min_f(g, -10, 10, eps)
        x0 = x
        x = x - gr * lam
        points.append(np.copy(x))
        if abs(x[0] - x0[0]) < eps and abs(x[1] - x0[1]) < eps:
            break
    return x, steps, points


def descent_gradient(grad, x, eps, n=1000):
    steps = 0
    points = [np.copy(x)]
    for i in range(1, n + 1):
        steps += 1
        l = 1 / 20
        x0 = x
        x = x - grad(x) * l
        points.append(np.copy(x))
        if abs(x[0] - x0[0]) < eps and abs(x[1] - x0[1]) < eps:
            break
    return x, steps, points

def conjugate_gradient(func, grad, x0, eps, min_f, n=100):
    k = 0
    xk = x0
    pk = -grad(x0)
    steps = 0
    points = [np.copy(x0)]
    while True:
        steps += 1
        alpha = min_f(lambda a: func(xk + a * pk), 0, 1, eps)
        xk1 = xk + alpha * pk
        points.append(np.copy(xk1))
        if math.sqrt((xk1[0] - xk[0])**2 + (xk1[1] - xk[1])**2) < eps:
            return xk1, steps, points
        if k + 1 == n:
            k = 0
            pk = -grad(xk1)
        else:
            beta = (np.linalg.norm(grad(xk1)) ** 2) / (np.linalg.norm(grad(xk)) ** 2)
            pk1 = -grad(xk1) + beta * pk
            pk = pk1
            k += 1
        xk = xk1


def powell_method(f, x, eps, min_f):  # Пауэлл
    n = len(x)
    D = np.eye(n)
    steps = 0
    points = [np.copy(x)]
    while True:
        steps += 1
        r = min_f(lambda l: f(x + l * D[:, n - 1]), -10, 10, eps)
        x = x + r * D[:, n - 1]
        points.append(np.copy(x))
        y = x
        for i in range(n):
            r = min_f(lambda l: f(x + l * D[:, i]), -10, 10, eps)
            x = x + r * D[:, i]
        for i in range(n - 1):
            D[:, i] = D[:, i + 1]
        D[:, n - 1] = x - y
        diff = 0
        for j in range (n - 1):
            diff += D[j, n - 1] ** 2
        if math.sqrt(diff) < eps:
            return x, steps, points


def newton(grad, hesse, x0, eps, n=100):
    steps = 0
    points = [np.copy(x0)]
    for _ in range(n):
        steps += 1
        g = -1 * grad(x0)
        h = hesse(x0)
        s = np.linalg.solve(h, g)
        x = x0 + s
        points.append(np.copy(x))
        if math.sqrt((x0[0] - x[0])**2 + (x0[1] - x[1])**2) < eps:
            return x, steps, points
        x0 = x


def make_field(f):
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)

    X, Y = np.meshgrid(x, y)
    Z = f([X, Y])
    return X, Y, Z


def draw_level_lines(func, points: list):
    x, y, z = make_field(func)
    points_x, points_y = [], []
    for p in points:
        points_x.append(p[0])
        points_y.append(p[1])
    fig, ax = plt.subplots()
    ax.contour(x, y, z)
    ax.scatter(points_x, points_y,
               c=[random() for _ in range(len(points_x))])
    ax.plot(points_x, points_y, c='red')
    plt.show()


def do_report(func, t):
    ans, steps, points = t
    print(f"Answer is: {ans} steps are: {steps}")
    draw_level_lines(func, points)


def generate_matrix(n, k):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = randint(1, k)
    i = randint(0, n - 1)
    matrix[i][i] = k
    j = i
    while j == i:
        j = randint(0, n - 1)
    matrix[j][j] = 1
    return matrix


def generate_function(n, k):
    matrix = generate_matrix(n, k)
    b = [randint(0, 100) for _ in range(n)]
    func = lambda x: sum(x[i] ** 2 * matrix[i][i] - b[i] * x[i] for i in range(n))
    return func



def n_by_k(n):
    fig, ax = plt.subplots()
    s = [0] * 10000
    for j in range(2, 20):
        func = generate_function(n, j * 40)
        grad = Gradient(func)
        start = np.array([randint(-10000, 10000) for _ in range(n)])
        ans, steps, points = steepest_descent_gradient(func, grad, start, 0.001, FuncMinimization.Fibonacci, 10000)
        s[j] = steps
        print(f"{j*40} = {steps}")
    y = [0]
    x = [0]
    ax.plot(x, y, color='red')
    for i in range(2, 19):
        y = [s[i], s[i + 1]]
        x = [i * 40, ((i + 1)*40)]
        ax.plot(x, y, color='red')
    plt.show()


def test_on(func, grad, hesse, x0, eps, min_f, ans):
    # print("test all functions on x0 = {x0} eps = {eps}\n  ans = {ans}")
    # print(f"steepest descent method = ", end="")
    # do_report(func, steepest_descent_gradient(func, grad, np.copy(x0), eps, min_f))
    # print(f"descent_gradient = ")
    # do_report(func, descent_gradient(grad, np.copy(x0), 20, eps))
    print("Conjugate gradient method")
    do_report(func, conjugate_gradient(func, grad, np.copy(x0), eps, min_f, 2))
    # print(f"pavel_method = ", end="")
    # do_report(func, pavel_method(func, grad, np.copy(x0), eps, min_f))
    print("Newton")
    do_report(func, newton(grad, hesse, np.copy(x0), eps))


def main():
    def func(x):
        return 7 * x[0] ** 2 + 2 * x[1] ** 2 + 2 * x[0] * x[1] + 9 * x[0] + 3 * x[1]
        # return 6 * x[0]**2 - 4 * x[0]*x[1] + 3 * x[1]**2 + 4 * math.sqrt(5) * (x[0] + 2 * x[1]) + 22
        # return np.sin(x[0]) + x[1] ** 2

    def grad(x):
        return np.array([14 * x[0] + 2 * x[1] + 9, 2 * x[0] + 4 * x[1] + 3])
        # return np.array([12*x[0] - 4 * x[1] + 4 * math.sqrt(5), -4 * x[0] + 6 * x[1] + 8 * math.sqrt(5)])
        # return np.array([np.cos(x[0]), 2*x[1]])

    def hesse(x):
        return np.array([[14, 2], [2, 4]])
        # return np.array([[12, -4], [-4, 6]])
        # return np.array([[-np.sin(x[0]), 0], [0, 2]])

    # n_by_k(5)
    test_on(func, grad, hesse, np.array([1000.0, 1000.0]), 0.001, FuncMinimization.Fibonacci, [-0.08695585, -0.43478307])



if __name__ == '__main__':
    main()
