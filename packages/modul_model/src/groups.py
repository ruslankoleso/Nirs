class Group:
    def __init__(self, id=None):
        self.id = id

    def setMiddleLevel(self):
        middle = 0
        allHours = 0
        for lesson in self.listLesson:
            middle += lesson.level_lesson*lesson.hourLesson
            allHours+=lesson.hourLesson
        self.middleLesson = middle / allHours
    def getListLesson(self):
        return self.listLesson

    def setListLesson(self,listLesson):
        self.listLesson = listLesson
