# -*- coding: utf-8 -*-
# Arlen Mateus Mendes - 201520121
# Luiz Otavio Soares - 201810544

import sys
import pandas as pd

filePath = str(sys.argv[1])

data = pd.read_excel(filePath, sheet_name='Dados')
config = pd.read_excel(filePath, sheet_name='Configuracoes')
restrictionsTeachers = pd.read_excel(filePath, sheet_name='Restricao')
restrictionsClass = pd.read_excel(filePath, sheet_name='Restricoes Turma')
preferences = pd.read_excel(filePath, sheet_name='Preferencias')

# Esta funcao constroi a matriz de horarios de Preferencias e de Restricoes passadas


def creatematrixSchedules(dataToBuild):
    matrixRestrictions = {}

    for index, row in dataToBuild.iterrows():

        if row[0] not in matrixRestrictions.keys():
            matrixRestrictions[row[0]] = {}

        if row[2] not in matrixRestrictions[row[0]].keys():
            matrixRestrictions[row[0]][row[2]] = []

        if row[1] not in matrixRestrictions[row[0]][row[2]]:
            matrixRestrictions[row[0]][row[2]].append(row[1].strftime("%H:%M"))

    return matrixRestrictions


matrixRestrictionsTeachers = creatematrixSchedules(restrictionsTeachers)
matrixPreferencesTeachers = creatematrixSchedules(preferences)
matrixRestrictionsClasses = creatematrixSchedules(restrictionsClass)

# Aqui é criado um vetor de Configuracoes
settings = []
for index, row in config.iterrows():

    if row[0] not in settings:
        settings.append(str(row[0]))

classDisciplineOfTeachers = {}
for index, row in data.iterrows():
    if row[2] not in classDisciplineOfTeachers.keys():
        classDisciplineOfTeachers[row[2]] = {}

    if row[1] not in classDisciplineOfTeachers[row[2]]:
        classDisciplineOfTeachers[row[2]][row[1]] = {}

    if row[0] not in classDisciplineOfTeachers[row[2]][row[1]]:
        classDisciplineOfTeachers[row[2]][row[1]][row[0]] = row[3]


def verifyIfTeacherHaveRestriction(teacher, day, schedule):

    if teacher in matrixRestrictionsTeachers.keys() and day in matrixRestrictionsTeachers[teacher].keys() and matrixRestrictionsTeachers[teacher] and schedule in matrixRestrictionsTeachers[teacher][day]:
        return True
    else:
        return False


print(verifyIfTeacherHaveRestriction('Professor 1', 'Terça', '10:40'))


class Teacher:
    def __init__(self, name, restrictions, preferences, classDiscipline):
        self.name = name
        self.restrictions = restrictions
        self.preferences = preferences
        self.classDiscipline = classDiscipline


class Vertex:
    def __init__(self, teacher, schoolClass, schedule):
        self.teacher = teacher
        self.schoolClass = schoolClass
        self.schedule = schedule
