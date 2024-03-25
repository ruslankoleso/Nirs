class Prepod:
    def __init__(self, id=None, name=None, wishes=None):
        self.id = id;
        self.name = name;
        self.wishes = wishes


class Wishes:
    def __init__(self, week=None):
        self.monday = week[0]
        self.tuesday = week[1]
        self.wensday = week[2]
        self.thursday = week[3]
        self.friday = week[4]
        self.saturday = week[5]
