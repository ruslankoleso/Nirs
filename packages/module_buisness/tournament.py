import math

from package.data_module.data.SheduleClass import Shedule
def selTournament(ind1:Shedule , ind2:Shedule):
    if math.fabs(ind1.fit - ind2.fit) == 1:
        return  [ind1,ind2]
    if ind1.fit > ind2.fit:
        return ind2
    if ind1.fit < ind2.fit:
        return ind1
    if ind1.fit == ind2.fit:
        return [ind1,ind2]
