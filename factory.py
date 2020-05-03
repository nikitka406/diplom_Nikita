from math import *
import csv

v = 50  # скорость ТС
car_cost = 10000  # цена за арнеду машины
penalty = 5  # штраф за превышения временного срока

# N = 10  # число объектов
# K = 5  # набор всех ТС
#
# OX = [0, -27, 21, 50, 31, -25, 31, -43, -35, -14]  # координаты по ОХ
# OY = [0, -44, 38, 42, 30, 39, 15, -23, 28, 20]  # координаты по ОУ
#
# d = [[0 for j in range(N)] for i in range(N)]  # расстояния между городами
# for i in range(N):
#     for j in range(N):
#         d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))
#
# t = d  # время перемещения между городами
# for i in range(N):
#     for j in range(N):
#         t[i][j] = round(t[i][j] / 24)
#
# wells = [0, 1, 2, 1, 3, 1, 1, 1, 5, 1]  # число скважин на i объекте
#
# S = [0 for j in range(N)]  # число рабочих дней для одного ТС для выполнения всех работ на i объекте
# for i in range(N):
#     S[i] = wells[i] * 2
#
# KA = 0  # кол-во ТС = кол-ву скважин
# for i in range(N):
#     KA += wells[i]
#
# e = [0, 7, 4, 8, 9, 7, 8, 3, 9, 8]  # начало работы на i объекте
# l = [0 for j in range(N)]  # конец работы на i объекте
# for i in range(N):
#     l[i] = e[i] + S[i]


# Создаем пустые списки для входных данных
path = "input/50/"
OX = []
OY = []
S = []
wells = []
e = []
l = []
N = 0
K = 0

# Читаем файл с клиентами
FILENAME1 = path + "customers1.csv"

with open(FILENAME1) as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row[0] != 'Name':
            OX.append(float(row[1]))
            OY.append(float(row[2]))
            S.append(float(row[3]))
            wells.append(int(row[4]))
            e.append(float(row[5]))
            l.append(float(row[6]))
            N += 1

OX.reverse()
OY.reverse()
S.reverse()
wells.reverse()
e.reverse()
l.reverse()

# Читаем файл с машинками, из него берем координаты для депо и добавляем в конец,
# для депо ставим 0 работ , 0 скважин и нулевое время
FILENAME2 = path + "vehicles1.csv"

with open(FILENAME2) as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row[0] == 'Vehicle 1':
            OX.append(float(row[1]))
            OY.append(float(row[2]))
            S.append(0)
            wells.append(0)
            e.append(0)
            l.append(0)
            N += 1

        # Считаем кол-во машин
        if row[0] != 'Name':
            K += 1

KA = 0  # кол-во ТС = кол-ву скважин
for i in range(N):
    KA += wells[i]

# Теперь разворачиваем решение чтобы депо было в начале
OX.reverse()
OY.reverse()
S.reverse()
wells.reverse()
e.reverse()
l.reverse()

# Строим матрицу расстояний и времени
d = [[0 for j in range(N)] for i in range(N)]  # расстояния между городами
for i in range(N):
    for j in range(N):
        d[i][j] = 111.1 * acos(sin(OX[i]) * sin(OX[j]) + cos(OX[i]) * cos(OX[j]) * cos(OY[j] - OY[i]))
        # d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))

t = [[0 for j in range(N)] for i in range(N)]  # время перемещения между городами
for i in range(N):
    for j in range(N):
        t[i][j] = (d[i][j] * 40) / (v * 24)

# клиента для стартового решения
param_population = int(N / 2)  # параметр который будет показывать, кол-во особей в популяции
param_min_num_cl_in_car = 8  # параметр отвечающий за, сколько минимально клиентов может присутствовать в однрой машине
param_crossing = param_population * 3  # сколько раз будем скрещивать решения
coins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Значение монетки, сколько значений такая вероятность

#
# print("d = ")
# for i in range(N):
#     for j in range(N):
#         print(d[i][j], end=' ')
#     print('\n')
# print('\n')
# print("t = ")
# for i in range(N):
#     for j in range(N):
#         print(t[i][j], end=' ')
#     print('\n')
# print('\n')
#
# for i in range(N):
#     print(OX[i], " ", OY[i], " ", S[i], " ", wells[i], " ", e[i], " ", l[i])
# print(K)
# print(KA)
