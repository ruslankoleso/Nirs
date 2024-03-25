from package.data_module.data.SheduleClass import Shedule
import random

def mutShuffleIndexes(individual:Shedule, probability):
    for group in individual.hromosoma:
        #выбираем сколько будем менять значений рандомно
        size = len(individual.hromosoma[group][0])
        #находим число заменяемых пар
        countMutLesson = random.randint(0,int(size / 2))
        #находим индексы сменяемых значений
        indexesMutant = random.sample(range(size), countMutLesson)
        #заменяемые значения
        swap_indx =  random.sample(range(size), countMutLesson)
        #вероятность мутации для группы
        probabilityCurrentGroup = random.random()
        if probabilityCurrentGroup < probability:
            for twoWeek in individual.hromosoma[group]:
                for i in range(0,countMutLesson):
                    twoWeek[indexesMutant[i]], twoWeek[swap_indx[i]] = \
                            twoWeek[swap_indx[i]], twoWeek[indexesMutant[i]]
    return individual