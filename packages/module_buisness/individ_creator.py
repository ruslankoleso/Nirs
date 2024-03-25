from package.data_module.data.getData import Data

data = Data()

def individCreator(self):
    # создаем расписание на 2 недели(четная, нечетная)
    # сначала делаем первую неделю, вставляем в расписание как countweek/2 пересчитываем часы, а потом строим дополнительную неделю
    ind = []
    flug = 1
    for i in range(len(self.x)):
        if i == len(self.x) - 1:
            flug1 = flug
            ind.append(flug1)
            break
        flug1 = random.uniform(0, flug)
        ind.append(flug1)
        flug -= flug1
    fitness = self.fitness(ind)
    return Individ(fitness, np.array(ind))

import random
import numpy as np
import openpyxl as op


class Lessons:
    """Класс описывающий занятия"""

    def __init__(self, data):
        """lesson- все слловари, чтобы задавать какие вообще есть предметы, какие проблемы и тд
            teacher-расписание преподавателей для каждого занятия
            wishes- пожелания преподавателей для начала, сами зададим
            1-не хочет
            0-хочет
            (в день какой)
            penalties- штрафы за неудобность расписания занятий
            count_-список,23 количество каждого предмет в неделю
        """
        self.groups = data.listGroup
        # self.sovmesn_par =
        self.week = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}
        self.dict_of_prepandlesson = dict_of_prepandlesson
        self.count_ = count_
        self.wishes = wishes
        self.penalties_weight = penalties_weight
        # максимальное количсетво пар в день
        self.maxlesson = 4
        self.maxsublesson = 3
        """Словарь занятий"""
        self.dict_of_lessons = dict_of_lessons
        """Словарь преподавателей"""
        self.dict_of_prepods = dict_of_prepods

    def __len__(self):
        # Возвращает значение самого старшего номера названияя предмета
        return len(self.dict_of_lessons)

    def getCost(self, lessonlist):
        """Получение всех штрафов """
        summand1 = self.Сalculation_Of_Fines_According_To_Wishes(lessonlist)
        summand2 = self.Calculat_penalties_weight(lessonlist)
        summand3 = self.Calculat_penalties_count(lessonlist)
        summand4 = self.Calculat_smejn_lesson(lessonlist)
        summand5 = self.Calculat_sovmestn_lessons(lessonlist)
        summand6 = self.Cal_more_two_lesson(lessonlist)
        return summand2 + summand1 + summand3 + summand4 + summand5 + summand6

    # lessons=[[1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11,1],
    # [12,12,13,14,15,16,17,18,19,12,13,14,12,13,14,15,16,17,18,19,18,13,14]]

    def Cal_more_two_lesson(self, lessonlist):
        func = 0

        for t in range(0, len(lessonlist)):
            for i in range(0, 6):
                for j in range(0, 1):
                    if i == 5:
                        if lessonlist[t][i * 4:i * 4 + 3].count(lessonlist[t][i * 4:i * 4 + 3][j]) == 3:
                            func += 100 / 50
                    if lessonlist[t][i*4:i*4 + 4].count(lessonlist[t][i*4:i*4 + 4][j]) == 3:
                        func += 100/50
        return func



    def Сalculation_Of_Fines_According_To_Wishes(self, lessonslist):
        """Вычисление функции по пожиланиям"""
        func = 0
        k = 0
        l = 0
        for i in range(0, len(lessonslist)):
            for j in lessonslist[i]:
                # сначала достаем из номера препдмета личный номер препода
                # затем через личный номер препода обращаемся к его пожеланиям
                # потом смотрим какой день недели сейчас и по нему делаем вывод

                if (k == 4):
                    k = 0
                    l += 1
                if self.wishes[self.dict_of_prepandlesson[i][j]][l] == 0:
                    func += 0.16
                k += 1
            k = 0
            l = 0
        return func

    def Calculat_penalties_weight(self, lessonslist):
        """Вычисление по уровню сложности предметов"""
        func = 0

        k = 0
        for i in range(0, len(lessonslist)):
            for j in lessonslist[i]:
                k += 1

                if self.penalties_weight[i][self.dict_of_lessons[i][j]] >= 9 and (k == 1 or k == 2):
                    func += (self.penalties_weight[i][self.dict_of_lessons[i][j]] * 0.1)/50
                    func -= 0.1
                if self.penalties_weight[i][self.dict_of_lessons[i][j]] >= 6 and k == 1:
                    func += self.penalties_weight[i][self.dict_of_lessons[i][j]] * 0.2 /50
                elif self.penalties_weight[i][self.dict_of_lessons[i][j]] >= 6 and k == 2:
                    func += self.penalties_weight[i][self.dict_of_lessons[i][j]] * 0.5/50
                else:
                    func += self.penalties_weight[i][self.dict_of_lessons[i][j]]/50
                if k == 4:
                    k = 0
            k = 0
        return func

    """Функцию, которая будет ограничивать колличество предметов всего должное в неделе"""

    def Calculat_penalties_count(self, lessonslist):
        func = 0
        for j in range(0, len(lessonslist)):
            for i in range(1, len(self.dict_of_lessons[j]) + 1):
                countJ = 0
                countJ += lessonslist[j].count(i)
                # добавления штрафа, если число не совпадает с требуемым
                if countJ != self.count_[j][i - 1]:
                    func += 1000/50

        return func

    # Функция, которая соединяет совместные пары вместе
    def Calculat_smejn_lesson(self, lessonlist):
        func = 0
        k = 1
        for j in range(0, len(lessonlist)):
            for i in range(0, 22):
                if k == 4:
                    k = 1
                    continue
                if (lessonlist[j][i] == lessonlist[j][i+1]):
                    func -= 110/50
                try:
                    if k == 1 or k == 2:
                        if lessonlist[j][i] == lessonlist[j][i+1] == lessonlist[j][i + 2]:
                            func += 120/50
                except IndexError:
                    pass
                k += 1
        return func

    # Функция, отвечающая за неповторение в одно время пар у разных групп
    def Calculat_sovmestn_lessons(self, lessonlist):
        func = 0
        for sovmest in self.sovmesn_par:
            list_sovm_group = list(sovmest)
            group1 = list_sovm_group[0]
            group2 = list_sovm_group[1]
            index_sovmest_lesson_group1 = []
            for index, meaning in enumerate(lessonlist[group1]):
                if meaning == sovmest[group1]:
                    index_sovmest_lesson_group1.append(index)
            for index, meaning in enumerate(lessonlist[group2]):
                if meaning == sovmest[group2]:
                    if not(index in index_sovmest_lesson_group1):
                        func +=100/50
        flug = 0
        for i in range(0, len(lessonlist)-1):
            for j in range(0, 23):
                if (self.dict_of_prepandlesson[i][lessonlist[i][j]] == self.dict_of_prepandlesson[i + 1][lessonlist[i + 1][j]]) :
                    for sovmest in self.sovmesn_par:
                        list_sovm_group = list(sovmest)
                        group1 = list_sovm_group[0]
                        group2 = list_sovm_group[1]
                        if group1 == i and group2 == i+1:
                            if lessonlist[i][j] == sovmest[group1] and lessonlist[i + 1][j] == sovmest[group2]:
                                flug = 1
                                break
                    if not(flug):
                        func +=150/50
                        flug = 0
        return func

    # Надо написать функцию, которая ппоказывает рассписание

    def printLection(self, lessonlist, func, i):
        wb = op.Workbook()
        sh1 = wb.get_sheet_by_name('Sheet')
        sh1.append((func,))
        for group in (self.groups):
            sh1.append(('Группа', group,))

        for index, group in enumerate(self.groups):
            wb.create_sheet(f'Группа {group}')
            sh1 = wb.get_sheet_by_name(f'Группа {group}')
            k = 1
            j = 1
            for t in lessonlist[index]:
                if k == 1:
                    print('\n{0}'.format(self.week[j]))
                    sh1.append((self.week[j],))
                lesson = self.dict_of_lessons[index][t]
                prepod = self.dict_of_prepods[self.dict_of_prepandlesson[index][t]]
                sh1.append((k, lesson, prepod,))
                print('{0}. {1} --- {2} '.format(k, lesson, prepod), end=' ')
                k += 1
                if k == 5:
                    k = 1
                    j += 1
            k = 1
            j = 1

        wb.save(f'Расписание--{func}-{i}.xlsx')


"""Функция генерирущая хромосомы"""


def Generation():
    data = Data()
    allHromo = []

    for group in data.listGroup:
        hromo = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        for lesson in group.listLesson:
            for countMiddleHourLesson in range(lesson.middleHour):
                index = random.randint()
                if hromo[index] == -1:
                    hromo[index] == lesson.id
                    lesson.hourLesson -=2
    return hromo


def mutShuffleIndexes1(individual, indpb):
    size = len(individual[0])
    for j in range(0, len(individual)):
        for i in range(size):
            if random.random() < indpb:
                swap_indx = random.randint(0, size - 2)
                if swap_indx >= i:
                    swap_indx += 1
                individual[j][i], individual[j][swap_indx] = \
                    individual[j][swap_indx], individual[j][i]

    return individual,


def cxTwoPointEnd(count_, ind1, ind2, ):
    size = 23


    # ind1 = [[],[]]
    for i in range(0, len(ind1)):
        probability = random.randint(0, 10)
        if probability >= 5:
            continue
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:  # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1
        ind1[i][cxpoint1:cxpoint2], ind2[i][cxpoint1:cxpoint2] \
            = ind2[i][cxpoint1:cxpoint2], ind1[i][cxpoint1:cxpoint2]

    # count_ = [[2, 3, 1, 3, 2, 2, 2, 2, 2, 2, 2],
    #          [2, 3, 1, 4, 2, 2, 2, 2, 2, 1, 2]]
    for j in range(0, len(count_)):
        for i in range(1, len(count_[j]) + 1):
            if ind1[j].count(i) > count_[j][i - 1]:
                delta = ind1[j].count(i) - count_[j][i - 1]
                ploxoi = i  # предмет, который превышает
                # Нашли все индексы расположения предмета, которого количсетво превышает допустимого
                indexes = []
                for p in range(0, len(ind1[j])):
                    if ind1[j][p] == ploxoi:
                        indexes.append(p)
                # Ищем предмет, которого мало
                for t in range(1, len(count_[j]) + 1):
                    if delta == 0:
                        break
                    if ind1[j].count(t) < count_[j][t - 1]:
                        delta2 = count_[j][t - 1] - ind1[j].count(t)
                        good = t  # хороший предмет, которого мало
                        # берем индекс предмета, который превышает количество и на его место ставим предмет, которого мало
                        for _ in range(0, delta2):
                            delta -= 1
                            indexdelete = random.randint(0, len(indexes) - 1)
                            ind1[j][indexes[indexdelete]] = good
                            indexes.pop(indexdelete)
                            if delta == 0:
                                break

    for j in range(0, len(count_)):
        for i in range(1, len(count_[j]) + 1):  # для второго индивидуума аналогично
            if ind2[j].count(i) > count_[j][i - 1]:
                delta = ind2[j].count(i) - count_[j][i - 1]
                ploxoi = i  # предмет, который превышает
                # Нашли все индексы расположения предмета, которого количсетво превышает допустимого
                indexes = []
                for p in range(0, len(ind2[j])):
                    if ind2[j][p] == ploxoi:
                        indexes.append(p)
                # Ищем предмет, которого мало
                for t in range(1, len(count_[j]) + 1):
                    if delta == 0:
                        break
                    if ind2[j].count(t) < count_[j][t - 1]:
                        delta2 = count_[j][t - 1] - ind2[j].count(t)
                        good = t  # хороший предмет, которого мало
                        # берем индекс предмета, который превышает количество и на его место ставим предмет, которого мало
                        for _ in range(0, delta2):
                            delta -= 1
                            indexdelete = random.randint(0, len(indexes) - 1)
                            ind2[j][indexes[indexdelete]] = good
                            if delta == 0:
                                break
    return ind1, ind2
