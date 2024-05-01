import psycopg2
from package.modul_model.src.groups import Group
from package.modul_model.src.lessons import Lesson
from package.modul_model.src.join_lesson import JoinLesson
from package.modul_model.src.prepods_wishes import Wishes, Prepod
from collections import defaultdict
class Data:
  def __init__(self, allWeek = None):
    self.login = 'postgres'
    self.password = "Tank__26rus"
    self.allWeek = allWeek
    self.getChetNechet()
    self.con()
    self.listGroups = self.setgroup()
    self.listPrepods = self.setListPrepods()
    self.setLessons()
    self.dictLessonPrepod = self.getLessonPrepod()
    self.dictPrepodWishes = self.getWishes()
    self.dictWeightLesson = self.getWeightLesson()
    self.dictLessonCount = self.getLessonCount()
    self.dictNamePrepod = self.getNamePrepod()
    self.dictNameLesson = self.getNameLesson()
    self.listJoinLesson = self.getJoinLesson()
      #получаем для всех предметов среднее число занятий в неделю(часы делим на два академических часа)
    # self.setMiddleHourForLesson(clearWeek+holidayWeek)

  def  getJoinLesson(self):
      self.cur.execute("select * from public.joint_couples ")
      joinLessons = self.cur.fetchall()
      listJoinLesson = []
      dictJoinLesson = defaultdict(list)
      for lesson in joinLessons:
        listJoinLesson.append(JoinLesson(idGroup1=lesson[0],idGroup2=lesson[1], idLesson1=lesson[2], idLesson2=lesson[3], idJoin=lesson[4]))
        dictJoinLesson[lesson[0]].append(lesson[2])
        dictJoinLesson[lesson[1]].append(lesson[3])
      self.dictJoinLesson = dictJoinLesson
      return listJoinLesson
  def getChetNechet(self):
      nechet = 0
      chet = 0
      if self.allWeek % 2 == 0:
          self.chet = self.nechet = self.allWeek / 2
      else:
          self.nechet = round(self.allWeek / 2) + 1
          self.chet = round(self.allWeek / 2)

  def con(self):
      self.conn = psycopg2.connect(user=f"{self.login}",
                                   password=f"{self.password}",
                                   port="5432",
                                   database="postgres")
      self.cur = self.conn.cursor()
#инициализая групп, создание списка групп
  def setgroup(self):
    self.cur.execute("select * from public.groups order by id_group")
    groups = self.cur.fetchall()
    listGroups= []
    for group in groups:
      listGroups.append(Group(id=int(group[0])))
    return listGroups

  # инициализируем преподавателей, создаем список Prepods
  def getListPrepods(self):
    return self.listPrepods
  def setListPrepods(self):
    self.cur.execute("select * from public.prepods order by id_prepod")
    prepods = self.cur.fetchall()
    listPrepods = []
    for prepod in prepods:
      self.cur.execute(f"select * from public.wishes where id_prepod = {prepod[0]}")
      wishes = self.cur.fetchall()

      classPrepod = Prepod(id=prepod[0], name=prepod[1], wishes=wishes[0][1:])
      listPrepods.append(classPrepod)
    return listPrepods

    #инициализация занятий

  def setLessons(self):
    self.cur.execute("select * from public.lessons order by (id_group,  id_lesson)")
    list_lessons = self.cur.fetchall()
#в класс каждой группы добавляем занятия
    for group in self.listGroups:
      listLesson = []
      for lesson in list_lessons:
          for prepod in self.listPrepods:
            if prepod.id == lesson[2]:
              if lesson[0] == group.id:
                  para = Lesson(id_lesson=lesson[1],
                                           level_lesson=lesson[3],
                                           prepod=prepod,
                                           hourLesson=int(lesson[5]/2),
                                           name=lesson[6],
                                           isLection=lesson[4],
                                           )
                  para.setMiddleHourNeChet(self.allWeek)

                  listLesson.append(para)

                  group.setListLesson(listLesson)



  def getsovmest_lesson(self):
    self.cur.execute("select * from public.joint_couples order by (id_group1,  id_group2)")
    list_sovmest_lesson = self.cur.fetchall()
    for row in list_sovmest_lesson:
      sovmest_lesson_now = {}
      group1 = self.groups.index(row[0])
      group2 = self.groups.index(row[1])
      sovmest_lesson_now[int(group1)] = int(row[2])
      sovmest_lesson_now[int(group2)] = int(row[3])
      self.main_sovmest_lesson.append(sovmest_lesson_now)

  def getWishes(self):

    dictPrepodWishes= {}
    for prepod in self.listPrepods:
        dictPrepodWishes[prepod.id] = prepod.wishes
    return dictPrepodWishes
  def getNamePrepod(self):
    dictNamePrepod = {}
    for prepod in self.listPrepods:
        prepod: Prepod
        dictNamePrepod[prepod.id] = prepod.name
    return dictNamePrepod
  def getLessonPrepod(self):
    dictLessonPrepod = {}
    for group in self.listGroups:
        dictLessonPrepod[group.id] = {}
        for lesson in group.listLesson:
            dictLessonPrepod[group.id][lesson.id_lesson] = lesson.id_prepod
    return dictLessonPrepod

  def getWeightLesson(self):

      dictWeightLesson = {}
      for group in self.listGroups:
          dictWeightLesson[group.id] = {}
          for lesson in group.listLesson:
              dictWeightLesson[group.id][lesson.id_lesson] = lesson.level_lesson
      return dictWeightLesson

  def getLessonCount(self):
      dictLessonCount = {}
      for group in self.listGroups:
          dictLessonCount[group.id] ={}
          for lesson in group.listLesson:
              dictLessonCount[group.id][lesson.id_lesson] = lesson.hourLesson
      return dictLessonCount
  def getNameLesson(self):
      dictNameLesson = {}
      for group in self.listGroups:
          group:Group
          dictNameLesson[group.id] = {}
          for lesson in group.listLesson:
              lesson:Lesson
              dictNameLesson[group.id][lesson.id_lesson] = lesson.name
      return dictNameLesson

