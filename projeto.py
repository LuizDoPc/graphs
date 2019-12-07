import sys
import pandas as pd
import math
import time
import plotly.graph_objects as go


startTime = time.time()

#####################################################
####         Importacao de dados                 ####
#####################################################

filePath = str(sys.argv[1])

data = pd.read_excel(filePath, sheet_name='Dados')
config = pd.read_excel(filePath, sheet_name='Configuracoes')
restrictionsTeachers = pd.read_excel(filePath, sheet_name='Restricao')
restrictionsClass = pd.read_excel(filePath, sheet_name='Restricoes Turma')
preferences = pd.read_excel(filePath, sheet_name='Preferencias')

#####################################################
####      Importacao de dados - fim              ####
#####################################################

#####################################################
####                Estruturas                   ####
#####################################################


class Vertex:
    def __init__(self, id, teacher, schoolClass, theme):
        self.id = id
        self.teacher = teacher
        self.schoolClass = schoolClass
        self.theme = theme
        self.restrictionsColors = []

        self.color = 0
        self.adjacents = []
        self.satur = 0
        self.degree = 0
        self.schedule = ''

    def addAdjacent(self, vertex):
        self.adjacents.append(vertex)
        self.degree += 1

    def getSatur(self):
        return self.satur

    def upSatur(self):
        self.satur += 1

    def downSatur(self):
        self.satur -= 1

    def addRestrictionColor(self, c):
        if c not in self.restrictionsColors:
            self.restrictionsColors.append(c)

    def upSaturAdjacents(self):
        for vertex in self.adjacents:
            vertex.upSatur()

    def addColorInRestricitionsColorsOfAdjacents(self, c):
        for vertex in self.adjacents:
            vertex.addRestrictionColor(c)

    def setColor(self, c):
        self.color = c
        self.upSaturAdjacents()
        self.addColorInRestricitionsColorsOfAdjacents(c)


#####################################################
####             Estruturas - fim                ####
#####################################################

#####################################################
#### Funcoes Genericas
#####################################################


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


def schedulesConfig():
    schedulesConf = []
    for _, s in config.iterrows():
        schedulesConf.append(s[0].strftime("%H:%M"))

    return schedulesConf


# Cria matriz de cores
def createColors():
    colors = {}

    weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    schedulesConf = schedulesConfig()
    color = 1
    for day in weekDays:
        for schedule in schedulesConf:
            colors[day + '-' + schedule] = color
            color += 1

    return colors


#####################################################
#### Funcoes Genericas - Fim
#####################################################

matrixRestrictionsTeachers = creatematrixSchedules(restrictionsTeachers)
matrixPreferencesTeachers = creatematrixSchedules(preferences)
matrixRestrictionsClasses = creatematrixSchedules(restrictionsClass)
colors = createColors()


def createGraph():
    graph = []
    # Cria grafo
    cont = 1
    for _, row in data.iterrows():
        for _ in range(int(row[3])):
            v = Vertex(cont, str(row[2]), row[1], str(row[0]))
            graph.append(v)
            cont += 1

    # Cria arestas/lista de adjacencia e adiciona a lista de restricoes de cores
    for i in graph:
        # arestas/lista de adjacencia
        for j in graph:
            if (i.id != j.id and
                (i.teacher == j.teacher or i.schoolClass == j.schoolClass)):
                i.addAdjacent(j)

        # Restricoes Professores
        if i.teacher in matrixRestrictionsTeachers:
            for day in matrixRestrictionsTeachers[i.teacher].keys():
                for schedule in matrixRestrictionsTeachers[i.teacher][day]:
                    if colors[day + '-' +
                              schedule] not in i.restrictionsColors:
                        i.addRestrictionColor(colors[day + '-' + schedule])

        # Restricoes Turmas
        if i.schoolClass in matrixRestrictionsClasses:
            for day in matrixRestrictionsClasses[i.schoolClass].keys():
                for schedule in matrixRestrictionsClasses[i.schoolClass][day]:
                    if colors[day + '-' +
                              schedule] not in i.restrictionsColors:
                        i.addRestrictionColor(colors[day + '-' + schedule])

    return graph

#####################################################
####         Funcoes de verificacao
#####################################################

def verifyNextTwoSchedules(vertex, color, graph, scheduleConfig):
    amountSchedulesPerDay = len(scheduleConfig)

    colorKey = ''
    for key, value in colors.items():
        if value == color:
            colorKey = key
            break

    if schedulesConfig()[amountSchedulesPerDay - 1] in colorKey:
        return True
    elif schedulesConfig()[amountSchedulesPerDay - 2] in colorKey:
        return True
    else:
        for v in graph:
            if v.theme == vertex.theme and v.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                if scheduleConfig.index(v.schedule.split('-')[1]) - 1 == scheduleConfig.index(colorKey.split('-')[1]):

                    for j in graph:
                        if j.theme == vertex.theme and j.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                            if scheduleConfig.index(j.schedule.split('-')[1]) - 2 == scheduleConfig.index(colorKey.split('-')[1]):
                                return False
    return True





#####################################################
####         Funcoes de verificacao - fim
#####################################################



#####################################################
####         Funcoes auxiliares Dsatur
#####################################################


def getBiggerSaturVertexId(graph):
    actual = None

    for ver in graph:
        if ver.color == 0 and (actual is None or ver.satur > actual.satur or
                               (ver.satur == actual.satur
                                and ver.degree > actual.degree)):
            actual = ver
    return actual


def allColorful(graph):
    for vertex in graph:
        if vertex.color == 0:
            return False
    return True


def toColor(vertex, graph, schedulesConfig):


    for color in colors.values():
        if verifyNextTwoSchedules(vertex, color, graph, schedulesConfig) and color not in vertex.restrictionsColors:
            vertex.setColor(color)
            break


#####################################################
####         Funcoes auxiliares Dsatur - Fim
#####################################################


def dsatur(graph):

    schedulesConfigVector = schedulesConfig()
    if allColorful(graph):
        return True
    while (allColorful(graph) == False):
        vertexBiggerSatur = getBiggerSaturVertexId(graph)
        # print(vertexBiggerSatur.id)
        # print(vertexBiggerSatur.schoolClass)
        # print(vertexBiggerSatur.satur)
        # print(vertexBiggerSatur.color)
        # print(vertexBiggerSatur)
        toColor(vertexBiggerSatur, graph, schedulesConfigVector)
    return True


graph = createGraph()

if dsatur(graph):

    print('bom')

    schoolClasses = {}
    for v in graph:
        for schedule, color in colors.items():
            if color == v.color:
                v.schedule = schedule

        if v.schoolClass in schoolClasses.keys():
            schoolClasses[v.schoolClass].append(v)
        else:
            schoolClasses[v.schoolClass] = [v]

    for sc, listSC in schoolClasses.items():
        listSC.sort(key=lambda s: s.color)

        week = {}

        for day in ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']:
            for scItem in listSC:
                if day in scItem.schedule:
                    if day not in week.keys():
                        week[day] = []
                    week[day].append(scItem)

        for day in week.keys():
            if len(week[day]) < len(schedulesConfig()):
                scheduleList = schedulesConfig()
                for i in range(len(scheduleList)):
                    foundClass = False
                    for cls in week[day]:
                        if cls is not None and scheduleList[i] in cls.schedule:
                            foundClass = True
                    if not foundClass:
                        week[day].insert(i, None)

        matrixPlot = [schedulesConfig()]

        for day in week.keys():
            textList = []
            for cls in week[day]:
                if cls is None:
                    textList.append(None)
                else:
                    textList.append(cls.teacher + ' - Matéria: ' + cls.theme)
            matrixPlot.append(textList)

        header = ["<b>" + str(sc) + "</b>"]
        for day in week.keys():
            header.append(day)

        fig = go.Figure(data=[go.Table(header=dict(values=header),cells=dict(values=matrixPlot))])
        fig.show()


else:
    print('Que merda!')

print("%s segundos - Tempo de execucao" % (time.time() - startTime))
