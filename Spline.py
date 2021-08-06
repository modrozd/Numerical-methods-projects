from matrices import matrix_methods, vector_methods, matrix_calculations
from matplotlib import pyplot
import csv
import os

def interpolation(points):
    def find_parameters():
        n = len(points)

        A = matrix_methods.matrix_zeros(4 * (n - 1), 4 * (n - 1))
        b = vector_methods.vec_zeros(4 * (n - 1))

        # Krok 1:
        # n przedziałów -> n-1 równań
        for i in range(n - 1):
            x, y = points[i]
            row = vector_methods.vec_zeros(4 * (n - 1))
            row[4 * i + 3] = 1
            A[4 * i + 3] = row
            b[4 * i + 3] = (float(y))

        # Krok 2:
        # n przedziałów -> n-1 równań
        # razem : 2n-2 równań
        for i in range(n - 1):
            x1, y1 = points[i + 1]
            x0, y0 = points[i]
            h = float(x1) - float(x0)
            row = vector_methods.vec_zeros(4 * (n - 1))
            row[4 * i] = h ** 3
            row[4 * i + 1] = h ** 2
            row[4 * i + 2] = h ** 1
            row[4 * i + 3] = 1
            A[4 * i + 2] = row
            b[4 * i + 2] = float(y1)

        # Krok 3:
        # n punktów -> n-2 wewnętrznych punktów -> n-2 równań
        # razem : 3n-4 równań
        for i in range(n - 2):
            x1, y1 = points[i + 1]
            x0, y0 = points[i]
            h = float(x1) - float(x0)
            row = vector_methods.vec_zeros(4 * (n - 1))
            row[4 * i] = 3 * (h ** 2)
            row[4 * i + 1] = 2 * h
            row[4 * i + 2] = 1
            row[4 * (i + 1) + 2] = -1
            A[4 * i] = row
            b[4 * i] = float(0)

        # Krok 4:
        # n punktów -> n-2 wewnętrznych punktów -> n-2 równań
        # razem : 4n-6 równań
        for i in range(n - 2):
            x1, y1 = points[i + 1]
            x0, y0 = points[i]
            h = float(x1) - float(x0)
            row = vector_methods.vec_zeros(4 * (n - 1))
            row[4 * i] = 6 * h
            row[4 * i + 1] = 2
            row[4 * (i + 1) + 1] = -2
            A[4 * (i + 1) + 1] = row
            b[4 * (i + 1) + 1] = float(0)

        # Krok 5: 2 równania
        # razem : 4n-4 równań

        # pierwszy
        row = vector_methods.vec_zeros(4 * (n - 1))
        row[1] = 2
        A[1] = row
        b[1] = float(0)

        # ostatni
        row = vector_methods.vec_zeros(4 * (n - 1))
        x1, y1 = points[-1]
        x0, y0 = points[-2]
        h = float(x1) - float(x0)
        row[1] = 2
        row[-4] = 6 * h
        A[-4] = row
        b[-4] = float(0)

        result = matrix_calculations.lu_factorization(A, b)
        return result

    parameters = find_parameters()

    def f(x):
        param_array = []
        row = []
        for param in parameters:
            row.append(param)
            if len(row) == 4:
                param_array.append(row.copy())
                row.clear()

        for i in range(1, len(points)):
            xi, yi = points[i-1]
            xj, yj = points[i]
            if float(xi) <= x <= float(xj):
                a, b, c, d = param_array[i-1]
                h = x - float(xi)
                return a*(h**3)+b*(h**2)+c*h+d

        return -123

    return f


def interpolate_using_spline(k):
    for file in os.listdir('./trasy'):
        f = open('./trasy/'+file, 'r', encoding="cp437", errors='ignore')
        dane = list(csv.reader(f))

        dane = dane[1:]
        shift = (-1)*(len(dane) % k)
        if shift != 0:
            dane_interpolacja = dane[:shift:k]
        else:
            dane_interpolacja = dane[::k]

        F = interpolation(dane_interpolacja)

        distance = []
        height = []
        interpolated_height = []
        for point in dane:
            x, y = point
            distance.append(float(x))
            height.append(float(y))
            interpolated_height.append(F(float(x)))

        train_distance = []
        train_height = []
        for point in dane_interpolacja:
            x, y = point
            train_distance.append(float(x))
            train_height.append(float(y))

        shift = -1 * interpolated_height.count(-123)

        pyplot.plot(distance, height, 'r.', label='dane csv')
        pyplot.plot(distance[:shift], interpolated_height[:shift], color='blue', label='uzyskana funkcja')
        pyplot.plot(train_distance, train_height, 'g.', label='dane do interpolacji')
        pyplot.legend()
        pyplot.ylabel('Wysokość')
        pyplot.xlabel('Odległość')
        pyplot.title('Przybliżenie funkcjami sklejanymi. ' + str(len(dane_interpolacja)) + ' węzłów')
        pyplot.suptitle(file)
        pyplot.grid()
        pyplot.show()