from package.data_module.data.getData import Data
from package.data_module.data.SheduleClass import Shedule
from package.module_buisness.mutation import mutShuffleIndexes
from package.module_buisness.tournament import selTournament
from package.module_buisness.crossing_of_individuals import crossingover
import copy
import random
import plotly.graph_objs as go
import plotly.offline as pyo
from package.module_buisness.obrabotkaShedule import obrabotka
import time

class Algorithm:
    def __init__(self,allWeek=None):
        self.data = Data(allWeek=allWeek)
        self.max_population = 2000

        self.len_population = 450
        self.count = 0
        self.minFit = 200
        self.bestShedule = 0
        self.Len_Hall_of_fame = 500
        self.probabilityMutation = 0.6
        self.probabilityCross = 0.9
        self.minFit = []
        self.meanFit = []

    def genetic(self):
        count = 0
        startTime = time.time()
        #Инициализируем популяцию
        offspring = self.getOffspring()
        self.createPodobie(offspring)
        self.Hall_of_Fame = self.Inithial_Hall_of_fame(offspring=offspring)
        self.Hall_of_Fame[0].getFit_opt()
        self.getMeanFit(offspring=offspring)
        self.getMinFitAndIndivid(offspring=offspring)
        countStop = 0
        fitStop = self.rangeHall_of_fame()[0]
        while self.max_population> count:
            count +=1
            self.createPodobie(offspring)
            #Селекция особей
            offspring1 = self.tournamentTwo(offspring)
            #Скрещивание особей
            # [-1, 8, -1, 9, 1, 3, 5, 7, 2, -1, 2, 11, 1, 4, -1, 5, 3, 2, 7, -1, 4, 10, 4]
            # [-1, 8, -1, 9, 1, 3, 5, -1, 4, 7, -1, 7, 4, 4, -1, 5, 3, 2, 7, -1, 4, 10, 4]
            # [-1, 8, -1, 9, 1, 3, 5, -1, 4, 7, 11, 7, 2, 2, -1, 5, 3, 2, 1, -1, 4, 10, 4]
            offspring2 = self.crossingover(copy.copy(offspring1))
            #Мутация особей

            # offspring3 = self.mutation(copy.copy(offspring2))
            # Дозакидываем особей из hall_of_fame
            offspring4 = self.addIndividFromHall_of_fame(offspring2)

            # Докидываем недостающие для размера популяции особей
            while len(offspring4) < self.len_population:

                offspring4.append(Shedule(copy.copy(self.data)))
            self.createPodobie(offspring4)
            for i in offspring4:
                if random.random() > 0.5:
                    obrabotka(i)
            # Находим среднее всей популяции
            self.getMeanFit(offspring=offspring4)
            # Находим min всей популяции
            self.getMinFitAndIndivid(offspring=offspring4)
            # Находим новых кандидатов для hall_of_fame
            self.getHall_of_fame(offspring4)
            offspring = offspring4
            minfit = self.Hall_of_Fame[0].fit
            print(minfit)
            # print(len(self.Hall_of_Fame[0].hromosomaWithWeek))
            # print(len(offspring))
            if fitStop == minfit:
                countStop +=1
            else:
                countStop=0
                fitStop = minfit
            if countStop == 100:
                break
            if count % 10 ==0:
                print(count)
                end_time = time.time()
                print('Время выполнение кода: ', end_time - startTime)
                #156.41606186318768
        # print(self.minInd.fit)
        min = self.rangeHall_of_fame()[0]
        optimalShedule = self.Hall_of_Fame[min]
        optimalShedule.getFit_opt()
        optimalShedule:Shedule
        optimalShedule.printLection()
        print(self.Hall_of_Fame[min].fit)
        obrabotka(optimalShedule)
        optimalShedule.getFit()
        print(optimalShedule.fit)
        self.graphix()

    def rangeHall_of_fame(self):
        listFitHall = []
        for i in self.Hall_of_Fame:
            listFitHall.append(i.fit)
        listRangeHall = []
        listFitHall.sort()
        for index in range(len(listFitHall)):
            for indexHall, i in enumerate(self.Hall_of_Fame):
                if i.fit == listFitHall[index]:
                    listRangeHall.append(indexHall)
        return listRangeHall

    def getHall_of_fame(self, offspring):
                #ранжируем hall_of_fame
        listRangeHall = self.rangeHall_of_fame()

        for  ind in offspring:
            ind:Shedule
            if self.Hall_of_Fame[listRangeHall[-1]].fit > ind.fit and ind.hromosomaWithWeek not in self.Hall_of_Fame:
                if ind not in self.Hall_of_Fame:
                    self.Hall_of_Fame.pop(listRangeHall[-1])
                    self.Hall_of_Fame.append(copy.copy(ind))
                    listRangeHall = self.rangeHall_of_fame()

    def addIndividFromHall_of_fame(self, offspring):
        # Дозакидываем особей из hall_of_fame
        for fame in self.Hall_of_Fame:
            fame: Shedule
            flugInOffspring = False
            for ind in offspring:
                ind: Shedule
                if ind.hromosomaWithWeek == fame.hromosomaWithWeek:
                    flugInOffspring = True
                    break
            if flugInOffspring == False:
                offspring.append(fame)
        return offspring
    def Inithial_Hall_of_fame(self, offspring):
        minListFit = []
        Hall_of_Fame = []
        for ind in offspring:
            minListFit.append(ind.fit)
        minListFit.sort()
        minListFit = minListFit[0:self.Len_Hall_of_fame]
        for ind in offspring:
            if ind.fit in minListFit:
                Hall_of_Fame.append(copy.copy(ind))

        return  Hall_of_Fame

    def createPodobie(self, offspring):
        for i in offspring:
            if random.random() > 0.6:
                i.podobie()

    def mutation(self,offspring):
        selectoffMut = []
        # мутация
        for ind in offspring:
            mutInd = mutShuffleIndexes(ind, self.probabilityMutation)
            if type(mutInd) is list:
                selectoffMut.append(mutInd[0])
                selectoffMut.append(mutInd[1])
            else:
                selectoffMut.append(mutInd)
        return  selectoffMut
    def tournamentTwo(self, offspring):
        # реализуем
        # турнирный
        # отбор
        selectoffspring = []
        indexTournier = random.sample(range(len(offspring)), len(offspring))
        for i in range(0, len(indexTournier) -1, 2):
            listTournir = selTournament(offspring[indexTournier[i]], offspring[indexTournier[i + 1]])

            if type(listTournir) is list:

                selectoffspring.append(listTournir[0])
                selectoffspring.append(listTournir[1])
            else:
                selectoffspring.append(listTournir)
        return  selectoffspring

    def crossingover(self, offspring):
        selectoffspringcross = []
        for i in range(0, len(offspring)-1, 2):
            if random.random() > self.probabilityCross:
                selectoffspringcross.append(offspring[i])
                selectoffspringcross.append(offspring[i + 1])
            else:
                ind1, ind2 = crossingover(copy.copy(offspring[i]), copy.copy(offspring[i + 1]), self.data)
                selectoffspringcross.append(ind1)
                selectoffspringcross.append(ind2)

        return  selectoffspringcross

    def getMeanFit(self, offspring):
        mean = 0
        for ind in offspring:
            mean += ind.fit
        self.meanFit.append(mean/len(offspring))

    def getMinFitAndIndivid(self, offspring):
        min = 400
        minInd = 0
        self.Hall_of_Fame
        for ind in offspring:
            if ind.fit < min:
                min = ind.fit
                minInd = copy.copy(ind)
        self.minFit.append(min)
        self.minInd = minInd

    def getOffspring(self):
        offspring = []
        while len(offspring) < self.len_population:
            shedule = Shedule(copy.copy(self.data))
            offspring.append(shedule)
        return  offspring
    def graphix(self):
        listPopulation = [i for i in range(self.max_population)]
        trace1 = go.Scatter(x=listPopulation, y=self.minFit, mode='lines', name='Минимальное значение штрафной функции')
        trace2 = go.Scatter(x=listPopulation, y=self.meanFit, mode='lines', name='Среднее значение штрафной функции')
        layout = go.Layout(
            title='Зависимость штрафной функции от поколения',
            xaxis={'title': 'Популяция'}, yaxis={'title': 'Значение штрафной функции'})
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        fig.update_layout(showlegend=True)
        fig.update_layout(
            legend=dict(
                orientation="h",
                y=-0.3,
                yanchor="bottom",
                x=0.5,
                xanchor="center"
            )
         )
        fig.write_image('график.jpg' , format='jpg', scale=2)
















