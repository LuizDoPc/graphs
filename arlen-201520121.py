# -*- coding: utf-8 -*-
# Arlen Mateus Mendes - 201520121
# Luiz Otavio Soares - 201810544

import sys
import pandas as pd
import math


def escreveArquivo():
    output_file = open('out.txt', "w+")
    for v in vertexList:
        if (v % int(math.sqrt(len(vertexList))) == 0 and v != 0):
            output_file.write("\n")
        output_file.write(v.cor)


# Esta funcao constroi a matriz de horarios de Preferencias e de Restricoes passadas
def creatematrixSchedules(dataToBuild):
    matrixRestrictions = {}

    for _, row in dataToBuild.iterrows():

        if row[0] not in matrixRestrictions.keys():
            matrixRestrictions[row[0]] = {}

        if row[2] not in matrixRestrictions[row[0]].keys():
            matrixRestrictions[row[0]][row[2]] = []

        if row[1] not in matrixRestrictions[row[0]][row[2]]:
            matrixRestrictions[row[0]][row[2]].append(row[1].strftime("%H:%M"))

    return matrixRestrictions


def createVertex():
    cont = 0
    for _, row in data.iterrows():
        for _ in range(int(row[3])):
            v = Vertex(cont, str(row[2]), str(row[1]), str(row[0]))
            vertexList.append(v)
            cont += 1


def fullColored():
    for v in vertexList:
        if v.color == -1:
            return False
    return True


def biggestSatur():
    bgSatur = 0
    bgId = 0
    for v in vertexList:
        if v.satur > bgSatur and v.color == -1:
            bgSatur = v.satur
            bgId = v.id
    return bgId


def dSatur():
    if fullColored():
        return True
    bgSatur = biggestSatur()
    possibleColors = vertexList[bgSatur].colors(int(math.sqrt(
        len(vertexList))))

    if possibleColors == -1:
        return False
    if not possibleColors:
        return False
    for c in possibleColors:
        vertexList[bgSatur].cor = c
        vertexList[bgSatur].upSaturAdj()
        if dSatur():
            return True
        else:
            vertexList[bgSatur].downSaturAdj()
            vertexList[bgSatur].cor = -1
    return False


#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################


class Vertex:
    def __init__(self, id, teacher, schoolClass, theme):
        self.teacher = teacher
        self.schoolClass = schoolClass
        self.theme = theme
        self.id = id

        self.color = -1
        self.adj = []
        self.satur = 0
        self.degree = 0

    def upSatur(self):
        self.satur += 1

    def downSatur(self):
        self.satur -= 1

    def upSaturAdj(self):
        for v in self.adj:
            v.upSatur()

    def downSaturAdj(self):
        for v in self.adj:
            v.downSatur()

    def calcSatur(self):
        for v in self.adj:
            if v.color != -1:
                self.satur += 1

    def addAdj(self, vertice):
        self.adj.append(vertice)
        self.degree += 1

    def colors(self, order):
        possibilities = list(range(1, order + 1))
        possibleValues = set(possibilities)
        jaExiste = set()
        for v in self.adj:
            if v.color == -1:
                continue
            jaExiste.add(int(v.color))
        possibleValues = possibleValues - jaExiste
        if (len(possibleValues) == 0):
            return -1
        return list(possibleValues)


#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

filePath = str(sys.argv[1])

data = pd.read_excel(filePath, sheet_name='Dados')
config = pd.read_excel(filePath, sheet_name='Configuracoes')
restrictionsTeachers = pd.read_excel(filePath, sheet_name='Restricao')
restrictionsClass = pd.read_excel(filePath, sheet_name='Restricoes Turma')
preferences = pd.read_excel(filePath, sheet_name='Preferencias')

vertexList = []

matrixRestrictionsTeachers = creatematrixSchedules(restrictionsTeachers)
matrixPreferencesTeachers = creatematrixSchedules(preferences)
matrixRestrictionsClasses = creatematrixSchedules(restrictionsClass)

#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

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

    if teacher in matrixRestrictionsTeachers.keys(
    ) and day in matrixRestrictionsTeachers[teacher].keys(
    ) and matrixRestrictionsTeachers[
            teacher] and schedule in matrixRestrictionsTeachers[teacher][day]:
        return True
    else:
        return False


#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

createVertex()

for i in vertexList:
    for j in vertexList:
        if (i.schoolClass == j.schoolClass
                or i.teacher == j.teacher) and i.id != j.id:
            if j not in i.adj:
                i.addAdj(j)
                j.addAdj(i)

if dSatur():
    escreveArquivo()
else:
    print('Erro')
