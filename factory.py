from math import sqrt
N = 10  # число объектов
K = 5  # набор всех ТС
car_cost = 1000 # цена за арнеду машины

OX = [0,-27,21,50,31,-25,31,-43,-35,-14]#координаты по ОХ
OY = [0,-44,38,42,30,39,15,-23,28,20]#координаты по ОУ

d = [[0 for j in range(N)] for i in range(N)]  # расстояния между городами
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))

t = d  # время перемещения между городами
for i in range(N):
    for j in range(N):
        t[i][j] = round(t[i][j] / 24)

wells = [0, 1, 2, 1, 3, 1, 1, 1, 5, 1]  # число скважин на i объекте

S = [0 for j in range(N)] # число рабочих дней для одного ТС для выполнения всех работ на i объекте
for i in range(N):
    S[i] = wells[i] * 2

KA = 0# кол-во ТС = кол-ву скважин
for i in range(N):
    KA += wells[i]

e = [0,7,4,8,9,7,8,3,9,8]  # начало работы на i объекте
l = [0 for j in range(N)]  # конец работы на i объекте
for i in range(N):
    l[i] = e[i] + S[i]