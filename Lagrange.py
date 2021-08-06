from matplotlib import pyplot
import csv
import os

def interpolation(points):
    def f(x):
        result = 0
        n = len(points)
        for i in range(n):
            xi, yi = points[i]
            base = 1
            for j in range(n):
                if i == j:
                    continue
                else:
                    xj, yj = points[j]
                    base *= (float(x) - float(xj))/float(float(xi) - float(xj))
            result += float(yi) * base
        return result
    return f


def interpolate_using_lagrange(k):
    for file in os.listdir('./trasy'):
        f = open('./trasy/'+file, 'r')
        dane = list(csv.reader(f))

        dane_interpolacja = dane[1::k]

        F = interpolation(dane_interpolacja)

        distance = []
        height = []
        interpolated_height = []
        for point in dane[1:]:
            x, y = point
            distance.append(float(x))
            height.append(float(y))
            interpolated_height.append(F(float(x)))

        train_distance = []
        train_height = []
        for point in dane_interpolacja:
            x, y = point
            train_distance.append(float(x))
            train_height.append(F(float(x)))

        pyplot.semilogy(distance, height, 'r.', label='dane csv')
        pyplot.semilogy(distance, interpolated_height, color='blue', label='uzyskana funkcja')
        pyplot.semilogy(train_distance, train_height, 'g.', label='dane do interpolacji')
        pyplot.legend()
        pyplot.ylabel('Wysokość')
        pyplot.xlabel('Odległość')
        pyplot.title('Przybliżenie interpolacją Lagrange\'a. ' + str(len(dane_interpolacja)) + ' węzłów')
        pyplot.suptitle(file)
        pyplot.grid()
        pyplot.show()
