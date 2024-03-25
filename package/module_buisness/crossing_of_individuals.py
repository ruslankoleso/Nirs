import copy
import random


from package.data_module.data.SheduleClass import Shedule
from package.data_module.data.getData import Data
from package.data_module.data.weekClass import weekShedule

def crossingover(ind1:Shedule, ind2:Shedule, data:Data):

    ind1 = Shedule(data=ind1.data, hromosomaWithWeekOld=copy.copy(ind1.hromosomaWithWeek), mapDictLessonCount=ind1.mapDictLessonCount, hromosoma=copy.copy(ind1.hromosoma))
    ind2 = Shedule(data=ind1.data, hromosomaWithWeekOld=copy.copy(ind2.hromosomaWithWeek), mapDictLessonCount=ind2.mapDictLessonCount, hromosoma=copy.copy(ind2.hromosoma))
    for group in ind1.hromosoma:

        indexCrosingover1 = random.randint(0, len(ind1.hromosoma[group][0]) - 1)
        indexCrosingover2 = random.randint(0, len(ind1.hromosoma[group][0]) - 1)
        indexCrosingover3 = random.randint(0, len(ind1.hromosoma[group][1]) - 1)
        indexCrosingover4 = random.randint(0, len(ind1.hromosoma[group][1]) - 1)
        if indexCrosingover1 > indexCrosingover2:
            indexCrosingover1, indexCrosingover2 = indexCrosingover2, indexCrosingover1
        if indexCrosingover1 == indexCrosingover2:
            indexCrosingover1 -= 1
        if indexCrosingover3 > indexCrosingover4:
            indexCrosingover3, indexCrosingover4 = indexCrosingover4, indexCrosingover3
        if indexCrosingover3 == indexCrosingover4:
            indexCrosingover3 -= 1
        for weekIndex in range(len(ind1.hromosoma[group])):
            # для четных одни точки, для нечетных другие
            if weekIndex%2 == 0:
                #меняем по точкам значения в двух хромосомах
                ind1.hromosomaWithWeek[group][weekIndex].week[indexCrosingover1:indexCrosingover2], ind2.hromosomaWithWeek[group][weekIndex].week[indexCrosingover1:indexCrosingover2], = \
                    ind2.hromosomaWithWeek[group][weekIndex].week[indexCrosingover1:indexCrosingover2], ind1.hromosomaWithWeek[group][weekIndex].week[indexCrosingover1:indexCrosingover2]
                #будем следить за тем, чтобы количество предметов было правильным

            if weekIndex%2 !=0:
                # меняем по точкам значения в двух хромосомах
                ind1.hromosomaWithWeek[group][weekIndex].week[indexCrosingover3:indexCrosingover4], ind2.hromosomaWithWeek[group][weekIndex].week[
                                                                                       indexCrosingover3:indexCrosingover4], = \
                    ind2.hromosomaWithWeek[group][weekIndex].week[indexCrosingover3:indexCrosingover4], ind1.hromosomaWithWeek[group][weekIndex].week[
                                                                                           indexCrosingover3:indexCrosingover4]
                # будем следить за тем, чтобы количество предметов было правильным отдельно для каждого индивидуума
    for group in ind1.hromosoma:
        for week in range(len(ind1.hromosomaWithWeek[group])):

            badLessonInd1 = {}
            goodLessonInd1 = {}
            badLessonInd2 = {}
            goodLessonInd2 = {}
            listLesson= list( ind1.dictWeightLesson[group].keys())# список всех предметов
            listLesson.append(-1)
            for lessonInd1, lessonInd2 in zip(listLesson, listLesson):

                lessonCountInd1 = ind1.hromosomaWithWeek[group][week].week.count(lessonInd1)
                lessonCountInd2 = ind2.hromosomaWithWeek[group][week].week  .count(lessonInd2)
                # смотрим для первого индивида
                try:
                    if lessonCountInd1 >= ind1.mapDictLessonCount[group][week][lessonInd1]:
                        badLessonInd1[lessonInd1] = lessonCountInd1 - ind1.mapDictLessonCount[group][week][lessonInd1]
                    if lessonCountInd1 < ind1.mapDictLessonCount[group][week][lessonInd1]:
                        goodLessonInd1[lessonInd1] = ind1.mapDictLessonCount[group][week][lessonInd1] - lessonCountInd1
                except:
                    if lessonCountInd1 >= 0:
                        badLessonInd1[lessonInd1] = lessonCountInd1 - 0
                    if lessonCountInd1 < 0:
                        goodLessonInd1[lessonInd1] = ind1.mapDictLessonCount[group][week][lessonInd1] - lessonCountInd1
                    #смотрим для второго индивида
                try:
                    if lessonCountInd2 >= ind2.mapDictLessonCount[group][week][lessonInd2]:
                        badLessonInd2[lessonInd2] =  lessonCountInd2 - ind2.mapDictLessonCount[group][week][lessonInd2]
                    if lessonCountInd2 < ind2.mapDictLessonCount[group][week][lessonInd2]:
                        goodLessonInd2[lessonInd2] =  ind2.mapDictLessonCount[group][week][lessonInd1] - lessonCountInd2
                except:
                    if lessonCountInd2 >= 0:
                        badLessonInd2[lessonInd2] = lessonCountInd2 - 0
                    if lessonCountInd2 < 0:
                        goodLessonInd2[lessonInd2] =ind2.mapDictLessonCount[group][week][lessonInd1] -lessonCountInd2
            # print('bad1',badLessonInd1)
            # print('good1',goodLessonInd1)
            # print('bad2', badLessonInd2)
            # print('good2', goodLessonInd2)
                    #для первого индивидуа замена предметов
            for lessonInd1 in badLessonInd1:
                for countLessonInd1 in range(badLessonInd1[lessonInd1]):
                    #находим случайный предмет которого не достает
                    if len(goodLessonInd1) == 0:
                        break
                    randomGoodLesson = random.choice(list(goodLessonInd1.keys()))
                    # находим индексы плохого предмета и заменяем его на хороший
                    badIndexes = [i for i in range(len(ind1.hromosomaWithWeek[group][week].week)) if ind1.hromosomaWithWeek[group][week].week[i] == lessonInd1]
                    badIndex = random.choice(badIndexes)
                    ind1.hromosomaWithWeek[group][week].week[badIndex] = randomGoodLesson
                    goodLessonInd1[randomGoodLesson] -=1
                    if goodLessonInd1[randomGoodLesson] ==0:
                        goodLessonInd1.pop(randomGoodLesson)

                    #для второго индивидуа замена предметов
            for lessonInd2 in badLessonInd2:
                for countLessonInd2 in range(badLessonInd2[lessonInd2]):
                    #находим случайный предмет которого не достает

                    randomGoodLesson = random.choice(list(goodLessonInd2.keys()))
                    # находим индексы плохого предмета и заменяем его на хороший
                    badIndexes = [i for i in range(len(ind2.hromosomaWithWeek[group][week].week)) if ind2.hromosomaWithWeek[group][week].week[i] == lessonInd2]
                    badIndex = random.choice(badIndexes)
                    ind2.hromosomaWithWeek[group][week].week[badIndex] = randomGoodLesson
                    goodLessonInd2[randomGoodLesson] -= 1
                    if goodLessonInd2[randomGoodLesson] == 0:
                        goodLessonInd2.pop(randomGoodLesson)

    ind1.setFit()
    ind2.setFit()
    return ind1, ind2


