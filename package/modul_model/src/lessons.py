import random


class Lesson:
    def __init__(self,
                 id_lesson=None,
                 level_lesson=None,
                 isLection=None,
                 hourLesson=None,
                 name=None,
                 prepod=None,
                 ):
        self.id_lesson = id_lesson
        self.id_prepod = prepod
        self.level_lesson = level_lesson
        self.isLection = isLection
        self.hourLesson = hourLesson
        self.name = name

    def setMiddleHourChet(self, countWeek):
        try:
            if random.random < 0.5:
                self.middleHour = round(self.hourLesson/countWeek)+1
            else:
                self.middleHour = int(self.hourLesson / countWeek)
        except:
            self.middleHour = 0
    def setMiddleHourNeChet(self, countWeek):
        try:
            if random.random < 0.5:
                self.middleHour = int(self.hourLesson / countWeek)
            else:
                self.middleHour = round(self.hourLesson / countWeek)
        except:
            self.middleHour = 0

    def __str__(self):
        print(f'{self.id_lesson}-{self.name}-{self.id_prepod}-prepod')