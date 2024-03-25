import copy


class weekShedule:
    def __init__(self, week = None, mapDictLessonCount = None):
        self.week = copy.copy(week)
        self.mapDictLessonCount = mapDictLessonCount
        self.fit = 0


