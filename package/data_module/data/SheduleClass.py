from package.data_module.data.getData import Data
from package.data_module.data.weekClass import weekShedule
from package.modul_model.src.lessons import Lesson
from package.modul_model.src.groups import Group
import random
import copy
import math
import openpyxl as op

from package.modul_model.src.join_lesson import JoinLesson


#Генерация особей

class Shedule:
    def __init__(self,data = None, hromosomaWithWeekOld=None, mapDictLessonCount=None, hromosoma=None):
        self.data = data

        self.dictPrepodWishes = data.dictPrepodWishes
        self.dictLessonPrepod = data.dictLessonPrepod
        self.dictWeightLesson = data.dictWeightLesson
        self.week = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}
        if hromosoma == None:
            self.hromosoma = self.Generation()
            self.mapDictLessonCount = self.setCountInWeekLesson()
        else:
            self.gethromosomaWithWeek(hromosomaWithWeekOld)
            self.hromosoma = hromosoma
            self.mapDictLessonCount = mapDictLessonCount

        self.fit = self.getFit()


    def gethromosomaWithWeek(self, hromosomaWithWeekOld):
        hromosomaWithWeekNew = {}
        for group in hromosomaWithWeekOld:
            hromosomaWithWeekNew[group] = []
            for indexweek in range(len(hromosomaWithWeekOld[group])):
                hromosomaWithWeekNew[group].append(
                    weekShedule(week=copy.copy(hromosomaWithWeekOld[group][indexweek].week), mapDictLessonCount=hromosomaWithWeekOld[group][indexweek].mapDictLessonCount))
        self.hromosomaWithWeek = hromosomaWithWeekNew


    def setFit(self):
        self.fit = self.getFit()
    def getFit_opt(self):
        fit =0
        fit += self.Fine_more_two_lesson()
        print(fit,  'после ,контроль больше 2 пар')
        fit += self.Calculat_penalties_weight()
        print(fit, 'после  тяжесть занятий')
        fit += self.Сalculation_Of_Fines_According_To_Wishes()
        print(fit, 'после  пожелания')
        fit += self.Calculat_penalties_count()
        print(fit, 'после  неправильное количесвто пар')
        fit += self.Calculat_smejn_lesson()
        print(fit, 'после  смежные пары')
        fit += self.Calculat_sovmestn_lessons()
        print(fit, 'после  совместные пары')
        fit += self.Calculat_nesovmest_lessons()
        print(fit, 'после  несовместные  пары')
    def getFit(self):
        fit =0
        fit += self.Fine_more_two_lesson()
        fit += self.Calculat_penalties_weight()
        fit += self.Сalculation_Of_Fines_According_To_Wishes()
        fit += self.Calculat_penalties_count()
        fit += self.Calculat_smejn_lesson()
        fit += self.Calculat_sovmestn_lessons()
        fit += self.Calculat_nesovmest_lessons()
        return   fit

    def Calculat_sovmestn_lessons(self):
        func = 0

        for sovmest in self.data.listJoinLesson:
            sovmest:JoinLesson

            group1 = sovmest.idGroup1
            group2 = sovmest.idGroup2
            index_sovmest_lesson_group1 = []
            for week1, week2 in zip(self.hromosomaWithWeek[group1],self.hromosomaWithWeek[group2]):
                index_sovmest_lesson_group1 = []

                for index, meaning1 in enumerate(week1.week):
                    if meaning1 == sovmest.idLesson1:
                        index_sovmest_lesson_group1.append(index)
                for index, meaning2 in enumerate(week2.week):
                    if meaning2 == sovmest.idLesson2:
                        if not (index in index_sovmest_lesson_group1):
                            func += 500 / 50
        return  func/self.data.allWeek
    #ПЕРЕПИСАТЬ. НУЖНО СОЗДАВАТЬ АВТОМАТИЧЕСКИ СЛОВАРЬ С НОМЕРАМИ ГРУПП, У КОТОРЫХ ОДИНАКОВЫЙ ПРЕПОДВАТЕЛЬ И ПРОВЕРЯТЬ ВЕДЕТ ЛИ ОН В ОДНО ВРЕМЯ ПАРЫ КАК АНАЛОГИЧНО НАВЕРХУ
    def Calculat_nesovmest_lessons(self):
        func = 0

        for group1 in self.hromosomaWithWeek:
            for indexweek, week in enumerate(self.hromosomaWithWeek[group1]):
                week: weekShedule
                for indexlesson, lesson in enumerate(week.week):
                    for group2 in self.hromosomaWithWeek:
                        if group1 == group2:
                            continue
                        if lesson == -1:
                            break
                        lessonOtherGroup = self.hromosomaWithWeek[group2][indexweek].week[indexlesson]
                        if lessonOtherGroup == -1:
                            continue
                        if (self.dictLessonPrepod[group1][lesson] == self.dictLessonPrepod[group2][lessonOtherGroup]):
                            flug = 0
                            for sovmest in self.data.listJoinLesson:
                                group1smech = sovmest.idGroup1
                                group2smech = sovmest.idGroup2
                                if group1smech == group1 and group2smech == group2:
                                    if lesson == sovmest.idLesson1 and lessonOtherGroup == sovmest.idLesson2:
                                        flug = 1
                                        break
                            if not (flug):
                                func += 150 / 50
                                flug = 0
        return func/self.data.allWeek
    def Calculat_smejn_lesson(self):
        func = 0
        k = 1
        for group in self.hromosomaWithWeek:
            for week in self.hromosomaWithWeek[group]:
                week: weekShedule
                for i in range(len(week.week)-1):
                    if k == 4:
                        k = 1
                        continue
                    if (week.week[i] == week.week[i + 1]):
                        func -= 50 / 50
                    try:
                        if k == 1 or k == 2:
                            if week.week[i] == week.week[i + 1] == week.week[i + 2]:
                                func += 100 / 50
                    except IndexError:
                        pass
                    k += 1
        return func/self.data.allWeek
    def setCountInWeekLesson(self):
        mapDictLessonCount = {}
        hromosomaWithWeek = {}
        for group in self.hromosoma:
            mapDictLessonCount[group] = {}
            hromosomaWithWeek[group] = []
            for indexweek in range(len(self.hromosoma[group])):
                mapDictLessonCount[group][indexweek] = {}
                for lesson in self.hromosoma[group][indexweek]:
                    mapDictLessonCount[group][indexweek][lesson] = self.hromosoma[group][indexweek].count(lesson)
                hromosomaWithWeek[group].append(weekShedule(week=self.hromosoma[group][indexweek], mapDictLessonCount=mapDictLessonCount[group][indexweek]))
        self.hromosomaWithWeek = hromosomaWithWeek
        return  mapDictLessonCount
    # Функция подсчитывающая пару, которая идет больше двух в день

    def Fine_more_two_lesson(self):
        """Функция подсчитывающая пару, которая идет больше двух в день"""
        funcAll = 0
        k = 0
        for group in self.hromosomaWithWeek:
            for week in self.hromosomaWithWeek[group]:
                week:weekShedule
                #при запуске вычисления полезности каждой недели надо обновлять значение
                week.fit = 0
                funcWeek = 0
                for day in range(0, 5):
                    for firstAndSecondLesson in range(0, 2):
                        if day == 5:
                            if week.week[day * 4:day * 4 + 3].count(week.week[day * 4:day * 4 + 3][0]) >= 3:
                                if week.week[day * 4:day * 4 + 4][firstAndSecondLesson] == -1:
                                    continue
                                funcWeek += 100 / 50

                        if week.week[day * 4:day * 4 + 4].count(week.week[day * 4:day * 4 + 4][firstAndSecondLesson]) >= 3:
                            if week.week[day * 4:day * 4 + 4][firstAndSecondLesson] == -1:
                                continue
                            funcWeek += 100 / 50
                week.fit += funcWeek
                funcAll +=funcWeek



        return funcAll /self.data.allWeek
    def gener_hromo_with_sovmest(self):
        map_hromo_group_nechet = {}
        map_hromo_group_chet = {}
        for group in self.data.listGroups:
            map_hromo_group_nechet[group.id] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            map_hromo_group_chet[group.id] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,-1, -1, -1]
        for sovmest in self.data.listJoinLesson:
            sovmest: JoinLesson
            group1 = sovmest.idGroup1
            group2 = sovmest.idGroup2
            lesson1 = sovmest.idLesson1
            lesson2 = sovmest.idLesson2
            #определяем объект группы по айди
            for group in self.data.listGroups:
                if group1 == group.id:
                    group1 = group
                    group1:Group
                elif group2 == group.id:
                    group2 = group
                    group2: Group
            # определяем объект занятия по айди
            for lesson in group1.listLesson:
                if lesson.id_lesson == lesson1:
                    lesson1=lesson
                    lesson1: Lesson
            for lesson in group2.listLesson:
                if lesson.id_lesson == lesson2:
                    lesson2=lesson
                    lesson2: Lesson
            #Если уже когда-то совместный предмет с другой группой был расставлен, то дорасставляем для другой группы также
            if lesson1.id_lesson in map_hromo_group_nechet[group1.id] and not lesson2.id_lesson in map_hromo_group_nechet[group2.id] :
                for i in range(0,23):
                    if lesson1.id_lesson == map_hromo_group_nechet[group1.id][i]:
                        map_hromo_group_nechet[group2.id][i] = lesson2.id_lesson
                        lesson2.hourLesson -= (self.data.nechet)
                    if lesson1.id_lesson == map_hromo_group_chet[group1.id][i]:
                        map_hromo_group_chet[group2.id][i] = lesson2.id_lesson
                        lesson2.hourLesson -= (self.data.chet )
                continue

            elif lesson2.id_lesson in map_hromo_group_nechet[group2.id] and not lesson1.id_lesson in map_hromo_group_nechet[group1.id]:
                for i in range(0,23):
                    if lesson2.id_lesson == map_hromo_group_nechet[group2.id][i]:
                        map_hromo_group_nechet[group1.id][i] = lesson1.id_lesson
                        lesson1.hourLesson -= (self.data.nechet)
                    if lesson2.id_lesson == map_hromo_group_chet[group2.id][i]:
                        map_hromo_group_chet[group1.id][i] = lesson1.id_lesson
                        lesson1.hourLesson -= (self.data.chet)
                continue




            count = max(lesson1.middleHour,lesson2.middleHour)
            indices1 = [i for i, x in enumerate(map_hromo_group_nechet[group1.id]) if x == -1]
            indices2 = [i for i, x in enumerate(map_hromo_group_nechet[group2.id]) if x == -1]

            indices3 = [i for i, x in enumerate(map_hromo_group_chet[group1.id]) if x == -1]

            indices4 = [i for i, x in enumerate(map_hromo_group_chet[group2.id]) if x == -1]

            indices = list(set(indices2) & set(indices1) &set(indices3) & set(indices4))

            index_lesson = random.sample(indices,count)
            for index in index_lesson:
                map_hromo_group_nechet[group1.id][index] = lesson1.id_lesson
                map_hromo_group_nechet[group2.id][index] = lesson2.id_lesson
            lesson1.hourLesson -= ( self.data.nechet *len(index_lesson))
            lesson2.hourLesson -= (self.data.nechet * len(index_lesson))
            #обновляем часы
            lesson1.setMiddleHourChet(self.data.chet)
            lesson2.setMiddleHourChet(self.data.chet)
            count_chet = max(lesson1.middleHour,lesson2.middleHour)
            #добавляем совместные пары в четные недели
            if len(index_lesson) < count_chet:
                new_indices =  [x for x in indices if x not in index_lesson]
                index_lesson.extend(random.sample(new_indices, count_chet-len(index_lesson)))
            if len(index_lesson) > count_chet:
                index_lesson = index_lesson[:count_chet]
            for index in index_lesson:
                map_hromo_group_chet[group1.id][index] = lesson1.id_lesson
                map_hromo_group_chet[group2.id][index] = lesson2.id_lesson
            lesson1.hourLesson -= (self.data.chet * len(index_lesson))
            lesson2.hourLesson -= (self.data.chet * len(index_lesson))
        return  map_hromo_group_nechet, map_hromo_group_chet
    def Generation(self):

        allWeek = self.data.allWeek

        allGroupGen = self.gener_hromo_with_sovmest()
        allGroupGen_new = {}
        # сделали две недели
        for group in self.data.listGroups:

            hromoTwoWeek = []
            hromoNechet = allGroupGen[0][group.id]
            for lesson in group.listLesson:
                if lesson.id_lesson in self.data.dictJoinLesson[group.id]:
                    continue
                for countMiddleHourLesson in range(lesson.middleHour):
                    # if no place
                    if hromoNechet.count(-1) == 0:
                        break

                    index = random.randint(0, 22)
                    while hromoNechet[index] != -1:
                        index = random.randint(0, 22)

                    hromoNechet[index] = lesson.id_lesson
                    lesson.hourLesson -= self.data.nechet
                    if lesson.hourLesson < self.data.nechet:
                        break

            hromoChet = allGroupGen[1][group.id]

            # добавили одну нечетную неделю


            for lesson in group.listLesson:

                if lesson.id_lesson in self.data.dictJoinLesson[group.id]:
                    continue

                for countMiddleHourLesson in range(lesson.middleHour):
                    index = random.randint(0, 22)
                    noPlace = False
                    while hromoChet[index] != -1:
                        index = random.randint(0, 22)
                        if hromoChet.count(-1) == 0:
                            noPlace = True
                            break
                    # если некуда вставлять
                    if noPlace:
                        break
                    hromoChet[index] = lesson.id_lesson
                    lesson.hourLesson -= self.data.chet
                    if lesson.hourLesson < self.data.chet:
                        break
                    # если все часы закончились
                    if lesson.hourLesson <= 0:

                        break

            # add new chet week

            # add all chet and nechet week
            for i in range(1, allWeek+1):
                if i %2 !=0:
                    hromoTwoWeek.append(copy.copy(hromoNechet))
                else:
                    hromoTwoWeek.append(copy.copy(hromoChet))

            allGroupGen_new[group.id] = hromoTwoWeek
            # После расставления происходит до закидывание и до удаление пар, которые нарушают план занятий
        for group in self.data.listGroups:
            for lesson in group.listLesson:
                #если пары совместные то удаляем их  конца
                if lesson.id_lesson in self.data.dictJoinLesson[group.id]:
                    if lesson.hourLesson < 0:
                        indexWeek = 1
                        while lesson.hourLesson < 0:

                            try:
                                last_idx = allGroupGen_new[group.id][-indexWeek][::-1].index(lesson.id_lesson)  # Находим индекс, начиная с конца списка
                                last_idx = len(allGroupGen_new[group.id][-indexWeek]) - last_idx - 1  # Получаем истинный индекс в исходном списке
                                allGroupGen_new[group.id][-indexWeek][last_idx] = -1
                                lesson.hourLesson += 1
                                indexWeek +=1
                            except:
                                indexWeek += 1
                    continue

                ListWeekDeleteLesson = []
                while lesson.hourLesson < 0:

                    # выбираем наши парные свдоенные недели в которой будем удалять предмет

                    indexWeek = random.randint(0, len(allGroupGen_new[group.id]) - 1)

                    while  (indexWeek in ListWeekDeleteLesson) and len(ListWeekDeleteLesson) != self.data.allWeek:
                        indexWeek = random.randint(0, len(allGroupGen_new[group.id]) - 1)

                    ListWeekDeleteLesson.append(indexWeek)
                    # выбираем место, где значения предмета
                    indexesDelete = [i for i, x in enumerate(allGroupGen_new[group.id][indexWeek]) if x == lesson.id_lesson]
                    count_while = 0
                    while len(indexesDelete) == 0 :
                        indexWeek = random.randint(0, len(allGroupGen_new[group.id]) - 1)
                        indexesDelete = [i for i, x in enumerate(allGroupGen_new[group.id][indexWeek]) if x == lesson.id_lesson]

                    lesson.hourLesson += 1
                    # выбираем какую пару удалим из расставленных пар конкретного предмета
                    index = random.choice(indexesDelete)
                    allGroupGen_new[group.id][indexWeek][index] = -1
        for group in self.data.listGroups:
            for lesson in group.listLesson:
                while lesson.hourLesson > 0:
                    if lesson.hourLesson <= len(allGroupGen_new[group.id]):

                        # выбираем недели в которые будем дозакидывать предметы
                        random_index = random.sample(range(len(allGroupGen_new[group.id])), lesson.hourLesson)
                        for indexAddInWeek in random_index:
                            # в конкретной недели находим, где есть пустые пары
                            indexesAdd = [i for i, x in enumerate(allGroupGen_new[group.id][indexAddInWeek]) if x == -1]
                            newIndexAddInWeek = -1
                            while len(indexesAdd) == 0:
                                # если пустых пар нет, то ищим в другой недели
                                newIndexAddInWeek = random.randint(0, len(allGroupGen_new[group.id]) -1)
                                indexesAdd = [i for i, x in
                                              enumerate(allGroupGen_new[group.id][newIndexAddInWeek])
                                              if x == -1]
                                # выбираем место из пустых пар и вставляем туда пару

                            if newIndexAddInWeek == -1:
                                indexAdd = random.choice(indexesAdd)
                                allGroupGen_new[group.id][indexAddInWeek][indexAdd] = lesson.id_lesson
                                lesson.hourLesson -=1
                            else:
                                indexAdd = random.choice(indexesAdd)
                                try:
                                    allGroupGen_new[group.id][newIndexAddInWeek][indexAdd] = lesson.id_lesson
                                    lesson.hourLesson -= 1
                                except:
                                    pass

                    if lesson.hourLesson > len(allGroupGen_new[group.id]):

                        # берем разницу между количеством часов и
                        differenceHour = lesson.hourLesson - len(allGroupGen_new[group.id])

                        random_index = random.sample(range(len(allGroupGen_new[group.id])), differenceHour)
                        for indexAddInWeek in random_index:
                            indexesAdd = [i for i, x in enumerate(allGroupGen_new[group.id][indexAddInWeek]) if x == -1]
                            indexAdd = random.choice(indexesAdd)
                            allGroupGen_new[group.id][indexAddInWeek][indexAdd] = lesson.id_lesson
                            lesson.hourLesson -= 1
        for group in self.data.listGroups:
            for lesson in group.listLesson:
                lesson.hourLesson = self.data.dictLessonCount[group.id][lesson.id_lesson]
                lesson.setMiddleHourNeChet(self.data.allWeek)

        return allGroupGen_new





#Функция учитывающая веса предметов и значение того, чтобы не было пар в конце дня
    def Calculat_penalties_weight(self):
        """Вычисление по уровню сложности предметов"""
        funcAll = 0
        k = 0

        nechet = 9
        for group in self.hromosomaWithWeek:

            for week in self.hromosomaWithWeek[group]:
                week:weekShedule
                funcWeek = 0
                for i ,lesson in enumerate(week.week):
                    k += 1
                    if lesson == -1:
                        if k == 1:
                            funcWeek +=350/50
                        if k == 2:
                            funcWeek +=350/50
                        if k == 3:
                            funcWeek += 100 / 50
                        if k==4:
                            pass
                        continue
                    funcWeek += (self.dictWeightLesson[group][lesson] * math.log(k+(math.exp(1) - 1.1)))/30
                    if k == 4:
                        k = 0
                    if i == 22:
                        k = 0
                funcAll+=funcWeek
                week.fit +=funcWeek
            k = 0
        return funcAll/self.data.allWeek


    def Сalculation_Of_Fines_According_To_Wishes(self):
        """Вычисление функции по пожиланиям"""
        funcAll = 0

        for group in self.hromosomaWithWeek:
            for week in  self.hromosomaWithWeek[group]:

                week :weekShedule
                funcWeek = 0
                k = 0
                l =1
                for lesson in week.week:
                    k +=1
                    #находим преподавателя, который ведет пару
                    if lesson == -1:
                        continue
                    prepod = self.dictLessonPrepod[group][lesson]
                    #смотрим в этот день хочет ли преподаватель вести пару
                    if self.dictPrepodWishes[prepod.id][(l)%6- 1]   != 1:
                        funcWeek += 100/50

                    if k == 4:
                        l +=1
                        k =0
                    if l == 5 and k == 3:
                        k = 0
                        l =0
                week.fit +=funcWeek
                funcAll +=funcWeek

        return  funcAll /self.data.allWeek

    def Counting_The_Number_Of_Lesson(self):

        mapCountLesson = {}
        for group in self.data.listGroups:
            mapCountLesson[group.id] = {}
            for lesson in group.listLesson:
                mapCountLesson[group.id][lesson.id_lesson] = 0
        for group in self.hromosoma:
            # подсчетали сколько в конкретной группе в семестре конкретных пар, записали их количество в словарь

            for week in self.hromosoma[group]:
                week : weekShedule
                mapCountInTwoWeek = {}
                for lesson in week:
                    lessonCount = week.count(lesson)
                    if lesson in mapCountInTwoWeek.keys():
                        continue
                    else:
                        mapCountInTwoWeek[lesson] = lessonCount

                for i in mapCountLesson[group]:
                    try:
                        mapCountLesson[group][i] += mapCountInTwoWeek[i]
                    except:
                        pass
        return mapCountLesson
    def Calculat_penalties_count(self):
        func = 0
        mapCountLesson = self.Counting_The_Number_Of_Lesson()
        #проверяем с получившимся словарем, сколько должно быть всего
        indexGroup = 0
        for group in self.hromosomaWithWeek:
            for index, i   in enumerate(self.data.listGroups):
                if group == i.id:
                    indexGroup = index

            for lessonId in self.data.dictLessonCount[group]:
                try:
                    if self.data.dictLessonCount[group][lessonId] != mapCountLesson[group][lessonId]:
                        func += 300/50
                        print(lessonId)
                        print(self.data.dictLessonCount[group][lessonId], "____" , mapCountLesson[group][lessonId])
                        print(group)
                except:
                    print(i)
        if func != 0 :
            print(self.data.dictLessonCount)
            print(mapCountLesson)
        return func /self.data.allWeek

    def podobie(self):
        for group in self.hromosomaWithWeek:
            dictPodobieWeek = {}
            for index, week in enumerate(self.hromosomaWithWeek[group]):
                week:weekShedule
                dictPodobieWeek[index] = []
                for nextindex,weeknext in enumerate(self.hromosomaWithWeek[group][index+1:]):
                    weeknext:weekShedule
                    flug = True
                    for i in dictPodobieWeek.values():
                        if nextindex + index + 1 in i or index in i:
                            flug =False
                            continue

                    if week.mapDictLessonCount == weeknext.mapDictLessonCount and flug == True:
                        dictPodobieWeek[index].append(nextindex+index+1)
            for podobieweek in dictPodobieWeek:
                bestWeek = 0
                minFitWeek = 0
                for i in dictPodobieWeek[podobieweek]:
                    bestWeek = self.hromosomaWithWeek[group][podobieweek]
                    minFitWeek = self.hromosomaWithWeek[group][podobieweek].fit
                    if self.hromosomaWithWeek[group][i].fit < minFitWeek:
                        minFitWeek = self.hromosomaWithWeek[group][i].fit
                        bestWeek = self.hromosomaWithWeek[group][i]
                for i in dictPodobieWeek[podobieweek]:
                    self.hromosomaWithWeek[group][i] = bestWeek
                    self.hromosomaWithWeek[group][i].fit = minFitWeek
                    self.hromosomaWithWeek[group][podobieweek] = bestWeek
                    self.hromosomaWithWeek[group][podobieweek].fit = minFitWeek
            self.setFit()
#Напишем функцию, которая выдает файл с расписанием
    def printLection(self):
        wb = op.Workbook()
        sh1 = wb.get_sheet_by_name('Sheet')
        sh1.append((self.fit,))
        for group in (self.data.listGroups):
            sh1.append(('Группа', group.id,))

        for index, group in enumerate(self.data.listGroups):
            wb.create_sheet(f'Группа {group.id}')
            sh1 = wb.get_sheet_by_name(f'Группа {group.id}')
            k = 1
            j = 1
            for week  in self.hromosomaWithWeek[group.id]:
                k = 1
                j = 1
                for lesson in week.week:
                    if k == 1:
                        sh1.append((self.week[j],))
                    if lesson != -1:
                        lessonNow = self.data.dictNameLesson[group.id][lesson]
                        prepod = self.data.dictLessonPrepod[group.id][lesson].name
                        sh1.append((k, lessonNow, prepod,))
                    else:
                        sh1.append((k, '----------------', '----------------',))
                    k += 1
                    if j ==6 and k == 3:
                        k == 1
                        j ==1
                    if k == 5:
                        k = 1
                        j += 1
            k = 1
            j = 1

        wb.save(f'Расписание для статьи 3 курса.xlsx')

