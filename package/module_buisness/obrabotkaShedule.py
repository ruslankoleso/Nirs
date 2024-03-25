import copy

from package.data_module.data.SheduleClass import Shedule
from package.data_module.data.weekClass import weekShedule
import math
def obrabotka(shed : Shedule):
    for groupId in shed.hromosomaWithWeek:
        k = 4
        for i in range(0,6):
            equivalenceClass = {}
            day_Class = {}
            for index, week in enumerate(shed.hromosomaWithWeek[groupId]):
                week: weekShedule
                if i == 5:
                    k = 3
                # для каждого дня i формируем словарь, где ключ номер недели, значение предметы и их количество
                day_Class[index] = {}
                for lesson in week.week[i * 4: i * 4 + k]:
                    day_Class[index][lesson] = week.week[i * 4: i * 4 + k].count(lesson)
            # после того как сформировали такое, объединяем в классы недели, у которых дни совпадают по предметам
            day_ClassNew = copy.copy((day_Class))
            for index, day in enumerate(day_Class):
                for dayNext in day_ClassNew:
                    if day_Class[day] == day_Class[dayNext]:
                        flug = True
                        for proverkaNalichi in equivalenceClass:
                            if dayNext  in equivalenceClass[proverkaNalichi]:
                                flug =False
                        if flug:
                            if str(day_Class[day]) in equivalenceClass.keys():
                                equivalenceClass[str(day_Class[day])].append(dayNext)
                            else:
                                equivalenceClass[str(day_Class[day])] = [day]
                                equivalenceClass[str(day_Class[day])] = [dayNext]

                day_ClassNew.pop(day)

            for classes in equivalenceClass:
                bestSolution = 0
                minSolution = 1000
                if len(equivalenceClass[classes]) <=1:
                    continue
                for element in equivalenceClass[classes]:
                    fit = fitDay(shed.hromosomaWithWeek[groupId][element].week[i * 4: i * 4 + k], shed,groupId)
                    if fit< minSolution:
                        bestSolution = shed.hromosomaWithWeek[groupId][element].week[i * 4: i * 4 + k]
                        # print('new fit ',fit, 'oldfit', minSolution)
                        minSolution = fit
                for element in equivalenceClass[classes]:
                    shed.hromosomaWithWeek[groupId][element].week[i * 4: i * 4 + k] = bestSolution
    return 0


def fitDay(day, shed, groupId):
    k=0
    funcDay = 0
    for lesson in day:
        k+=1
        if lesson == -1:
            if k == 1:
                funcDay += 350 / 50
            if k == 2:
                funcDay += 250 / 50
            if k == 3:
                funcDay += 150 / 50
            if k == 4:
                funcDay += 0
        else:
            funcDay += (shed.dictWeightLesson[groupId][lesson] * math.log(k + (math.exp(1) - 2)))/30
    return funcDay