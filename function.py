import random
import sys
import factory
from forFile import *
import csv


# красивая печать
def BeautifulPrint(X, Y, Sresh, A):
    for k in range(len(X[0][0])):
        print('Номер машины ', k)
        for i in range(factory.N):
            for j in range(factory.N):
                print(X[i][j][k], end=' ')
            print("\n")

        print("e = ", end=' ')
        for i in range(factory.N):
            print(factory.e[i], end=' ')
        print("\n")

        print("l = ", end=' ')
        for i in range(factory.N):
            print(factory.l[i], end=' ')
        print("\n")

        print("y = ", end=' ')
        for i in range(factory.N):
            print(Y[i][k], end=' ')
        print("\n")

        print("a = ", end=' ')
        for i in range(factory.N):
            print(A[i][k], end=' ')
            # for k in range(factory.KA):
            #     print(A[i][k], end=' ')
            # print("\n")
        print("\n")

        print("s = ", end=' ')
        for i in range(factory.N):
            print(Sresh[i][k], end=' ')
            # for k in range(factory.KA):
            #     print(Sresh[i][k], end=' ')
            # print("\n")
        print("\n")
    #
    # for i in range(factory.N):
    #     for k in range (factory.N):
    #        print(factory.t[i][k], end=' ')
    #     print('\n')

    # for i in range(factory.N):
    #     #     for k in range (factory.N):
    #     #         print(factory.d[i][k], end=' ')
    #     #     print('\n')


# красивая печать в файл
def BeautifulPrintInFile(lokal_X, lokal_Y, lokal_Sresh, lokal_A, target_function, number_solution):
    file = open('output/Population.txt', 'a')
    file.write('Номер решения ' + str(number_solution))
    file.write("\n")
    for k in range(len(lokal_X[0][0])):
        file.write('Номер машины ' + str(k))
        file.write("\n")
        for i in range(factory.N):
            for j in range(factory.N):
                file.write(str(lokal_X[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

        file.write("e = ")
        for i in range(factory.N):
            file.write(str(factory.e[i]) + ' ')
        file.write("\n")

        file.write("l = ")
        for i in range(factory.N):
            file.write(str(factory.l[i]) + ' ')
        file.write("\n")

        file.write("y = ")
        for i in range(factory.N):
            file.write(str(lokal_Y[i][k]) + ' ')
        file.write("\n")

        file.write("a = ")
        for i in range(factory.N):
            file.write(str(lokal_A[i][k]) + ' ')
            # for k in range(factory.KA):
            #     print(A[i][k], end=' ')
            # print("\n")
        file.write("\n")

        file.write("s = ")
        for i in range(factory.N):
            file.write(str(lokal_Sresh[i][k]) + ' ')
            # for k in range(factory.KA):
            #     print(Sresh[i][k], end=' ')
            # print("\n")
        file.write("\n")
    file.write(str(target_function))
    file.write("\n")
    file.write("\n")
    # for i in range(factory.N):
    #     for k in range (factory.N):
    #        file.write(factory.t[i][k]+' ')
    #     file.write('\n')

    # for i in range(factory.N):
    #     #     for k in range (factory.N):
    #     #         print(factory.d[i][k], end=' ')
    #     #     print('\n')
    file.close()


# Считаем кол-во используемых ТС
def AmountCarUsed(lokal_y):
    summa = 0  # счетчик
    amount = 0  # число машин
    for k in range(len(lokal_y[0])):
        for j in range(factory.N):
            summa += lokal_y[j][k]  # смотрим посещает ли К-ая машина хотя бы один город
        if summa != 0:  # если не 0 значит  посетила
            amount += 1  # прибавляем еденичку
        summa = 0  # Обнуляем счетчик
    return amount


# копирование решения
def CopyingSolution(local_x, local_y, local_s, local_a):
    local_X = local_x.copy()
    # local_X = [[[0 for k in range(len(local_x[0][0]))] for j in range(factory.N)] for i in
    #      range(factory.N)]  # едет или нет ТС с номером К из города I в J
    # # for k in range(factory.KA):
    # for i in range(factory.N):
    #     local_X[i] = list(local_x[i])
    #     for j in range(factory.N):
    #             local_X[i][j][k] = local_x[i][j][k]
    local_Y = local_y.copy()
    local_S = local_s.copy()
    local_A = local_a.copy()
    return local_X, local_Y, local_S, local_A


# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, pinalty_function=0):
    target_function = 0
    for k in range(len(x[0][0])):
        for i in range(factory.N):
            for j in range(factory.N):
                target_function += factory.d[i][j] * x[i][j][k]

    target_function += pinalty_function
    return target_function


# Распределяем на каждую локацию по машине
def OneCarOneLocation():
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(factory.KA)] for j in range(factory.N)] for i in
         range(factory.N)]  # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(factory.KA):
        y[0][k] = 1
    s = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    # поочереди отправляем ТС на локации, по одному на скважину
    k = 0
    for j in range(1, factory.N):
        if factory.wells[j] >= 1:
            for i in range(factory.wells[j]):
                x[0][j][k] = 1  # туда
                x[j][0][k] = 1  # обратно
                y[j][k] = 1
                if factory.wells[j] > 1:
                    s[j][k] = factory.S[j] / factory.wells[j]
                else:
                    s[j][k] = factory.S[j]

                if factory.e[j] > factory.t[0][j]:
                    a[j][k] = factory.e[j]
                    a[0][k] = a[j][k] + s[j][k] + factory.t[j][0]
                else:
                    a[j][k] = factory.t[0][j]
                    a[0][k] = a[j][k] + s[j][k] + factory.t[j][0]
                # print(a[j][k], end=' ')
                k += 1
            # print("\n")
    return x, y, s, a


# удаляем машину с локации если позволяют огр
def DeleteCarNonNarushOgr(sizeK):
    # Убираем одну машину
    for i in range(1, factory.N):
        # копии чтобы не испортить исходное решение
        lokal_X, lokal_Y, lokal_Sresh, lokal_A = ReadStartSolutionOfFile(sizeK)

        if factory.wells[i] > 1:  # Выбираем только те локации у которых больше одной скважины
            for k in range(sizeK - 1):
                if lokal_Y[i][k] == 1 and lokal_Y[i][k + 1] == 1:  # -//- ту машину за которой едет еще одна
                    lokal_Y[i][k] = 0
                    lokal_Y[0][k] = 0
                    lokal_Sresh[i][k + 1] += lokal_Sresh[i][k]
                    lokal_Sresh[i][k] = 0
                    lokal_A[i][k] = 0
                    lokal_X[0][i][k] = 0
                    lokal_X[i][0][k] = 0
                    # target_function -= car_cost
                    if VerificationOfBoundaryConditions(lokal_X, lokal_Y, lokal_Sresh, lokal_A) == 1:
                        # BeautifulPrint(lokal_X, lokal_Y, lokal_Sresh, lokal_A)
                        SaveStartSolution(lokal_X, lokal_Y, lokal_Sresh, lokal_A)
                        # Если ограничения не сломались то сохраняем эти изменения
                    else:
                        lokal_X, lokal_Y, lokal_Sresh, lokal_A = ReadStartSolutionOfFile(sizeK)


# перезапись одного маршрута на другой
def Rewriting(lokal, k, m, flag):
    if flag == "1":
        for j in range(factory.N):
            lokal[j][k] = lokal[j][m]
            lokal[j][m] = 0
    if flag == "2":
        for i in range(factory.N):
            for j in range(factory.N):
                lokal[i][j][k] = lokal[i][j][m]
                lokal[i][j][m] = 0


# TODO делит почему портит стартовое решение
# TODO надо полностью переписать делит с помощью флага и последующео удаления через remove
# удаляем/уменьшаем размерность с помощью не используемых машин
def DeleteNotUsedCar(lokal_x, lokal_y, lokal_s, lokal_a):
    # todo сейчас удаляются машину пока получается, надо чтобы оставались те которые наши(не арендованные) под
    #  вопросом?????
    for k in range(len(lokal_x[0][0])):
        summa1 = 0  # Обнуляем счетчик
        for j in range(1, factory.N):
            # смотрим посещает ли К-ая машина хотя бы один город
            summa1 += lokal_y[j][k]
        if summa1 == 0:  # если 0 значит не посещает
            if k != len(lokal_x[0][0]) - 1:  # если пустой машиной оказалась не последняя в списке, то
                for m in range(k + 1, len(lokal_x[0][0])):  # ищем ближайшую рабочую машину
                    summa2 = 0
                    for i in range(factory.N):
                        summa2 += lokal_y[i][m]
                    if summa2 != 0:  # сохранем ее в первый пустой маршрут
                        Rewriting(lokal_y, k, m, "1.txt")
                        Rewriting(lokal_s, k, m, "1.txt")
                        Rewriting(lokal_a, k, m, "1.txt")
                        Rewriting(lokal_x, k, m, "2")
                        break

            factory.KA = AmountCarUsed(lokal_y)
            if factory.KA > factory.K - 1:
                # создаем новые переменные так как они должны быть меньше по размерности относительно старых,
                # нельзя просто прировнять
                lokal_X = [[[0 for k in range(factory.KA)] for j in range(factory.N)] for i in
                           range(factory.N)]  # едет или нет ТС с номером К из города I в J
                lokal_Y = [[0 for k in range(factory.KA)] for i in
                           range(factory.N)]  # посещает или нет ТС с номером К объект i
                lokal_Sresh = [[0 for k in range(factory.KA)] for i in
                               range(factory.N)]  # время работы ТС c номером К на объекте i
                lokal_A = [[0 for k in range(factory.KA)] for i in
                           range(factory.N)]  # время прибытия ТС с номером К на объект i
                for k in range(factory.KA):
                    for i in range(factory.N):
                        for j in range(factory.N):
                            lokal_X[i][j][k] = lokal_x[i][j][k]
                        lokal_Y[i][k] = lokal_y[i][k]
                        lokal_Sresh[i][k] = lokal_s[i][k]
                        lokal_A[i][k] = lokal_a[i][k]
                return lokal_X, lokal_Y, lokal_Sresh, lokal_A
            else:
                print("NOTIFICATION from DeleteNotUsedCar: Уже удалены все арендованные машины")
                return lokal_x, lokal_y, lokal_s, lokal_a


# ищем минимальный путь по которому можно попасть в client
def SearchTheBestSoseda(client):
    neighbor = 0  # старый сосед
    bufer = factory.d[0][client]  # расстояние от старого сосед адо клиента
    for i in range(factory.N):
        if bufer >= factory.d[i][client] and i != client:
            # ищим мин расстояние до клиента с учетом что новый сосед не клиент
            bufer = factory.d[i][client]
            neighbor = i
    return neighbor


# номер машины которая обслуживает клиента
def NumberCarClienta(y, client):
    for k in range(len(y[0])):
        if y[client][k] == 1:
            return k


# узнаем про клиента, лист он или не лист
def ListOrNotList(y, a, client):
    k = NumberCarClienta(y, client)  # получаем номер машины, которая обслуживает этого клиента
    for i in range(1, factory.N):
        if a[client][k] < a[i][k]:  # Если у машины, котораяя посещает clienta есть город,
            return 1  # который она посещает позже, значит он НЕ ЛЕСИТ
    return 0  # значит клиент лист


# ищем соседа слева либо справа
def SearchSosedLeftOrRight(x, y, client, leftOrRight):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    if leftOrRight == "left":
        for i in range(factory.N):  # ищем по столбцу
            if x[i][client][k] == 1:
                return i
        return -1
    if leftOrRight == "right":
        for i in range(factory.N):  # ищем по строке
            if x[client][i][k] == 1:
                return i
        return -1
    if leftOrRight != "left" and leftOrRight != "right":
        print("ERROR from SearchSosedLeftOrRight: неверное значение переменной leftOrRight")


def CarIsWork(y, k):
    suma = 0
    for i in range(factory.N):
        if y[i][k] == 1:
            suma += 1

    if suma != 0:
        return 1
    else:
        return -1


# Рекурсия чтобы заполнить время прибытия
def RecursiaForTime(x, s, a, i, k, recurs):
    for j in range(factory.N):
        if x[i][j][k] != 0 and j != 0 and recurs < factory.N:
            # print("Нашли соседа для ", i, " справа ", j)
            # print("Время перемещения из ", i, " в ", j, " = ", factory.t[i][j])
            # если время прибытия меньше начала работ, то ждем
            if factory.e[j] > a[i][k] + s[i][k] + factory.t[i][j]:
                # print("Приехали слишком рано ждем")
                a[j][k] = factory.e[j]
                # print("a[j][k] = ", a[j][k])
            # иначе ставим время прибытия
            else:
                # print("Опоздали")
                a[j][k] = a[i][k] + s[i][k] + factory.t[i][j]
                # print("a[j][k] = ", a[j][k])

            recurs += 1
            RecursiaForTime(x, s, a, j, k, recurs)
        elif x[i][j][k] != 0 and j == 0 and recurs < factory.N:
            # print("Встретили ноль, пора заканчивать рекурсию")
            # print("Время прибытия в ", i, " = ", a[i][k])
            # print("Время работы в ", i, " = ", s[i][k])
            # print("Время переиещения из ", i, " в ", j, " = ", factory.t[i][j])

            a[j][k] = a[i][k] + s[i][k] + factory.t[i][j]

            # print("Время прибытия в депо = ", a[j][k])
            # for i in range(factory.N):
            #     print(a[i][k], end=' ')
            # print('\n')

            return True

        elif recurs > factory.N:
            return -1


# определяем время приезда на конкретную локацию
def TimeOfArrival(x, y, s):
    recurs = 0
    print("Начнем заполнять время прибытия")
    a = [[0 for k in range(len(s[0]))] for i in range(factory.N)]
    for k in range(len(s[0])):
        if CarIsWork(y, k) == 1:
            # print("ЗАходим в рекурсию")
            flag = RecursiaForTime(x, s, a, 0, k, recurs)
    if flag != -1:
        return a
    elif flag == -1:
        return flag


# удаляем клиента из выбранного  маршрут
def DeleteClientaFromPath(x, y, s, a, client):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right")  # ищем город после клиента
    # если у клиента есть сосед справо и слево
    if clientLeft != -1 and clientRight != -1:
        if clientLeft != clientRight:
            x[clientLeft][clientRight][k] = 1  # соединяем левого и правого соседа
        else:
            x[clientLeft][clientRight][k] = 0

        x[client][clientRight][k] = 0  # удаляем ребро клиента с правым соседом
        x[clientLeft][client][k] = 0  # удаляем ребро клиента с левым соседом

        # У и S для левого и правого не меняются, но время прибытия меняется
        y[client][k] = 0  # машина К больше не обслуживает клиента
        s[client][k] = 0  # время работы машины К у клиента = 0
        a[client][k] = 0  # машина не прибывает к клиенту
        # a = TimeOfArrival(x, y, s)
        # если удаляем клиента и остается только депо, ставим там 0
        summa = 0
        for i in range(1, factory.N):
            summa += y[i][k]
        if summa == 0 and y[0][k] == 1:
            y[0][k] = 0

    elif clientLeft == -1 or clientRight == -1:
        print("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")  # log
        raise IOError("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")

    return x, y, s, a


# штрафнвя функция
def PenaltyFunction(y, s, a, iteration):
    penalty_sum = 0
    fine = 0
    for i in range(factory.N):
        for k in range(len(a[i])):
            if a[i][k] + s[i][k] > factory.l[i]:
                # Если время окончания не совпадает с регламентом, то умножаем разницу во времени на коэффициент
                penalty_sum += max(0, ((a[i][k] + s[i][k]) - factory.l[i]) * factory.penalty * iteration)

    # если кол-во используемых ТС пока еще боьше чем число допустимых, тогда штрафуем
    if AmountCarUsed(y) > factory.K:
        fine = (AmountCarUsed(y) - factory.K) * factory.car_cost * iteration

    return penalty_sum + fine


# Создаем хранилище решений, для большего числа рещений
def SolutionStore(target_start, sizeK):
    # Хранилище решений, первый индекс это номер решения, со второго начинается само решение
    X = [0 for n in range(factory.param_population)]  # едет или нет ТС с номером К из города I в J
    for n in range(factory.param_population):
        X[n] = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in range(factory.N)]

    Y = [0 for n in range(factory.param_population)]  # посещает или нет ТС с номером К объект i
    for n in range(factory.param_population):
        Y[n] = [[0 for k in range(sizeK)] for i in range(factory.N)]

    Sresh = [0 for n in range(factory.param_population)]  # время работы ТС c номером К на объекте i
    for n in range(factory.param_population):
        Sresh[n] = [[0 for k in range(sizeK)] for i in range(factory.N)]

    A = [0 for n in range(factory.param_population)]  # время прибытия ТС с номером К на объект i
    for n in range(factory.param_population):
        A[n] = [[0 for k in range(sizeK)] for i in range(factory.N)]

    Target_Function = [target_start for n in
                       range(factory.param_population)]  # здесь сохраняем результат целевой функции для каждого решения

    SizeSolution = [sizeK for n in
                    range(factory.param_population)]  # здесь сохраняем размер каждого решения в популяции

    return X, Y, Sresh, A, Target_Function, SizeSolution


# Граничные условия
def X_join_Y(x, y):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(len(y[0])):
        for j in range(factory.N):
            for i in range(factory.N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                print("ERROR from X_join_Y: сломалось первое ограничение, несовместность переменных х, у")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, factory.N):
        if i != 0:
            for k in range(len(s[i])):
                bufer1 += s[i][k]
            if bufer1 != factory.S[i]:
                print("ERROR from V_jobs: сломалось второе ограничение, общий объем работ на объекте", i,
                      "не совпадает с регламентом")
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(y):
    bufer1 = 0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, factory.N):
        if i != 0:
            for k in range(len(y[i])):
                bufer1 += y[i][k]
            if bufer1 > factory.wells[i]:
                print("ERROR from TC_equal_KA: сломалось третье ограничение, кол-во ТС на одном объекте", i,
                      "больше чем число скважин")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, factory.N):
        for k in range(len(y[i])):
            if s[i][k] > factory.S[i] * y[i][k]:
                print("ERROR from ban_driling: сломалось четвертое ограничение, ТС не приехало на объект", i,
                      ", но начало бурение")
                return 0
    return 1


def window_time_down(a, y):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, factory.N):
        for k in range(len(y[i])):
            if factory.e[i] > a[i][k] and y[i][k] == 1:
                print("ERROR from window_time_down: сломалось пятое ограничение, время приезда на объкект", i,
                      "меньше чем начало работ")  # не работает ээто ограничение
                return 0
    return 1


def window_time_up(a, s, y):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, factory.N):
        for k in range(len(a[i])):
            if a[i][k] + s[i][k] > factory.l[i] and y[i][k] == 1:
                print("ERROR from window_time_up: сломалось шестое ограничение, время окончание работ на объкект", i,
                      "больше чем конец работ")
                return 0
    return 1


def ban_cycle(a, x, s, y):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1.txt-x[i][j][k])
    for i in range(1, factory.N):
        for j in range(1, factory.N):
            for k in range(len(a[0])):
                if a[i][k] - a[j][k] + x[i][j][k] * factory.t[i][j] + s[i][k] > factory.l[i] * (1 - x[i][j][k]) and \
                        y[i][k] == 1:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, машина", k,
                          "не посещает депо согласно временным рамкам")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(len(y[i])):
                if s[i][k] < 0 or a[i][k] < 0:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, неправельные значение переменных a, s")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, неправельное значение переменной x")
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, неправельное значение переменной y")
                    return 0
    return 1


# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a, pinalty="false"):
    # по дефолту смотрим все огр, но если тру то не рассматриваем огр на своевременный конец работ
    if pinalty == "false":
        result = X_join_Y(x, y) * V_jobs(s) * TC_equal_KA(y) * ban_driling(s, y) * \
                 window_time_down(a, y) * window_time_up(a, s, y) * \
                 ban_cycle(a, x, s, y) * positive_a_and_s(x, y, a, s)
    elif pinalty == "true":
        result = X_join_Y(x, y) * V_jobs(s) * TC_equal_KA(y) * ban_driling(s, y) * \
                 window_time_down(a, y) * \
                 positive_a_and_s(x, y, a, s)
    else:
        print("ERROR from VerificationOfBoundaryConditions: неверное значение, переменной pinalty")
        return -1
    if result == 1:
        return 1  # good
    else:
        return 0
