import numpy as np
import os

matrix = np.load("resources/matrix_43_2.npy")

size = len(matrix)

x = list()
y = list()
z = list()

limit = 504

for i in range(0, size):
    for j in range(0, size):
        if matrix[i][j] > limit:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("results/points_43", x=x, y=y, z=z)
np.savez_compressed("results/points_43_zip", x=x, y=y, z=z)

points_size = os.path.getsize('results/points_43.npz')
points_zip_size = os.path.getsize('results/points_43_zip.npz')
print(f"points = {points_size}")
print(f"points_zip = {points_zip_size}")

print(f"Сжатый файл весит на {points_size - points_zip_size} байт меньше")