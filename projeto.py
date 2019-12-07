import sys
import pandas as pd
import time
import plotly.graph_objects as go


#####################################################
####         Importacao de dados                 ####
#####################################################

filePath = str(sys.argv[1])

dataSchool = pd.read_excel(filePath, sheet_name='Dados')
config = pd.read_excel(filePath, sheet_name='Configuracoes')
restrictionsTeachers = pd.read_excel(filePath, sheet_name='Restricao')
restrictionsClass = pd.read_excel(filePath, sheet_name='Restricoes Turma')
preferencesTeachers = pd.read_excel(filePath, sheet_name='Preferencias')


#####################################################
####      Importacao de dados - fim              ####
#####################################################

#####################################################
####                Estruturas                   ####
#####################################################

class GlobalData:
    def __init__(self):
        self.settings = schedulesConfig()
        self.colorsSchedules = createColors(self.settings)
        self.colorsUsed = []
        self.matrixRestrictionsTeachers = creatematrixSchedules(restrictionsTeachers)
        self.matrixPreferencesTeachers = creatematrixSchedules(preferencesTeachers)
        self.matrixRestrictionsClasses = creatematrixSchedules(restrictionsClass)
        self.metedPreferences = {}

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
        self.preference = False

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

    # Usado exclusivamente por Dsatur
    def setColor(self, c):
        self.color = c
        self.upSaturAdjacents()



#####################################################
####             Estruturas - fim                ####
#####################################################

#####################################################
#### Funcoes Genericas
#####################################################


def creatematrixSchedules(dataToBuild):
    matrix = {}

    for _, row in dataToBuild.iterrows():

        if row[0] not in matrix.keys():
            matrix[row[0]] = {}

        if row[2] not in matrix[row[0]].keys():
            matrix[row[0]][row[2]] = []

        if row[1] not in matrix[row[0]][row[2]]:
            matrix[row[0]][row[2]].append(row[1].strftime("%H:%M"))

    return matrix


def schedulesConfig():
    schedulesConf = []
    for _, s in config.iterrows():
        schedulesConf.append(s[0].strftime("%H:%M"))

    return schedulesConf


# Cria matriz de cores
def createColors(schedulesConf):
    colors = {}

    weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    c = 1
    for day in weekDays:
        for schedule in schedulesConf:
            colors[day + '-' + schedule] = c
            c += 1

    return colors


#####################################################
#### Funcoes Genericas - Fim
#####################################################

def createVertexList():

    vertexList = []
    count = 1
    for _, row in dataSchool.iterrows():
        for _ in range(int(row[3])):
            v = Vertex(count, str(row[2]), row[1], str(row[0]))
            vertexList.append(v)
            count += 1

    return vertexList


def createGraph(data):
    graph = createVertexList()

    # Cria arestas/lista de adjacencia e adiciona a lista de restricoes de cores
    for i in graph:
        # arestas/lista de adjacencia
        for j in graph:
            if i.id != j.id and(i.teacher == j.teacher or i.schoolClass == j.schoolClass):
                i.addAdjacent(j)

        # Restricoes Professores
        if i.teacher in data.matrixRestrictionsTeachers:
            for day in data.matrixRestrictionsTeachers[i.teacher].keys():
                for schedule in data.matrixRestrictionsTeachers[i.teacher][day]:
                    if data.colorsSchedules[day + '-' + schedule] not in i.restrictionsColors:
                        i.addRestrictionColor(data.colorsSchedules[day + '-' + schedule])

        # Restricoes Turmas
        if i.schoolClass in data.matrixRestrictionsClasses:
            for day in data.matrixRestrictionsClasses[i.schoolClass].keys():
                for schedule in data.matrixRestrictionsClasses[i.schoolClass][day]:
                    if data.colorsSchedules[day + '-' + schedule] not in i.restrictionsColors:
                        i.addRestrictionColor(data.colorsSchedules[day + '-' + schedule])

    return graph


#####################################################
####         Funcoes de verificacao
#####################################################

def verifyNextTwoSchedules(vertex, color, graph, scheduleConfig):
    amountSchedulesPerDay = len(scheduleConfig)

    if amountSchedulesPerDay < 3:
        return True

    colorKey = ''
    for key, value in colors.items():
        if value == color:
            colorKey = key
            break

    if scheduleConfig[amountSchedulesPerDay - 1] in colorKey:
        return True
    elif scheduleConfig[amountSchedulesPerDay - 2] in colorKey:
        return True
    else:
        response = False
        for v in graph:
            if v.theme == vertex.theme and v.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                if scheduleConfig.index(v.schedule.split('-')[1]) - 1 == scheduleConfig.index(colorKey.split('-')[1]):

                    for j in graph:
                        if j.theme == vertex.theme and j.schoolClass == vertex.schoolClass and colorKey.split('-')[
                            0] in v.schedule:
                            if scheduleConfig.index(j.schedule.split('-')[1]) - 2 == scheduleConfig.index(
                                    colorKey.split('-')[1]):
                                response = False
        return response


def verifyTwoPreviousSchedules(vertex, color, graph, scheduleConfig):
    amountSchedulesPerDay = len(scheduleConfig)

    if amountSchedulesPerDay < 3:
        return True

    colorKey = ''
    for key, value in colors.items():
        if value == color:
            colorKey = key
            break

    if scheduleConfig[0] in colorKey:
        return True
    elif scheduleConfig[1] in colorKey:
        return True
    else:
        response = True
        for v in graph:
            if v.theme == vertex.theme and v.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                if scheduleConfig.index(v.schedule.split('-')[1]) + 1 == scheduleConfig.index(colorKey.split('-')[1]):

                    for j in graph:
                        if j.theme == vertex.theme and j.schoolClass == vertex.schoolClass and colorKey.split('-')[
                            0] in v.schedule:
                            if scheduleConfig.index(j.schedule.split('-')[1]) + 2 == scheduleConfig.index(
                                    colorKey.split('-')[1]):
                                response = False
        return response


def verifyNextAndPreviousSchedule(vertex, color, graph, scheduleConfig):
    amountSchedulesPerDay = len(scheduleConfig)

    if amountSchedulesPerDay < 3:
        return True

    colorKey = ''
    for key, value in colors.items():
        if value == color:
            colorKey = key
            break

    if scheduleConfig[0] in colorKey:
        return True
    elif scheduleConfig[amountSchedulesPerDay - 1] in colorKey:
        return True
    else:
        response = False
        for v in graph:
            if v.theme == vertex.theme and v.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                if scheduleConfig.index(v.schedule.split('-')[1]) - 1 == scheduleConfig.index(colorKey.split('-')[1]):

                    for j in graph:
                        if j.theme == vertex.theme and j.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                            if scheduleConfig.index(j.schedule.split('-')[1]) + 1 == scheduleConfig.index(colorKey.split('-')[1]):
                                response = False
        return response


#####################################################
####         Funcoes de verificacao - fim
#####################################################


#####################################################
####         Funcoes auxiliares Dsatur
#####################################################


def getBiggerSaturVertex(graph):
    actual = None

    for ver in graph:
        if ver.color == 0 and (actual is None or ver.satur > actual.satur or (ver.satur == actual.satur and ver.degree > actual.degree)):
            actual = ver
    return actual


def allColorful(graph):
    for vertex in graph:
        if vertex.color == 0:
            return False
    return True


def toColor(vertex, colorsUsed):
    c = 1
    valid = False
    while not valid:
        valid = True
        if c not in vertex.restrictionsColors:
            for adj in vertex.adjacents:
                if adj.color == c:
                    valid = False
                    break
            if valid:
                vertex.setColor(c)
                if c not in colorsUsed:
                    colorsUsed.append(c)

        else:
            valid = False

        c += 1


#####################################################
####         Funcoes auxiliares Dsatur - Fim
#####################################################


#####################################################
####         Algoritmos
#####################################################

def dsatur(graph, colorsUsed):
    while (allColorful(graph) == False):
        vertexBiggerSatur = getBiggerSaturVertex(graph)
        toColor(vertexBiggerSatur, colorsUsed)
    return True


def improvement(graph, data):

    reducedColors = []

    while reducedColors != data.colorsUsed:
        reducedColors = data.colorsUsed
        data.colorsUsed = []
        for c in reducedColors:
            for v in graph:
                if v.color == c:
                    i = 1
                    colorful = False
                    while i in data.colorsSchedules.values() and not colorful:
                        if v.color != i and i not in v.restrictionsColors and not v.preference:
                            valid = True

                            for adj in v.adjacents:
                                if adj.color == i:
                                    valid = False
                                    break

                            if valid:
                                v.color = i
                                colorful = True

                            if v.color not in data.colorsUsed:
                                data.colorsUsed.append(v.color)
                        i += 1


def setColorsPreferencesBeforeDsatur(graph, data):

    vertexByTecher = {}
    for v in graph:
        if v.teacher in vertexByTecher.keys():
            vertexByTecher[v.teacher].append(v)
        else:
            vertexByTecher[v.teacher] = [v]

    for teacher, vertexList in vertexByTecher.items():
        if teacher in data.matrixPreferencesTeachers.keys():
            if teacher in vertexByTecher.keys():
                preferences = data.matrixPreferencesTeachers[teacher]
                preferencesCount = 0
                preferencesMetedCount = 0
                notColorful = []
                for day in preferences.keys():
                    preferencesCount += len(preferences[day])
                    for schedule in preferences[day]:
                        color = data.colorsSchedules[day+'-'+schedule]
                        colorful = False

                        for v in vertexList:
                            if v.color == 0 and color not in v.restrictionsColors:
                                valid = True

                                for adj in v.adjacents:
                                    if adj.color == color:
                                        valid = False

                                if valid:
                                    v.setColor(color)
                                    v.preference = True
                                    preferencesMetedCount += 1
                                    colorful = True
                                    break

                        if not colorful:
                            notColorful.append('nao coloriu ' + str(color) + ' para ' + teacher)
                if preferencesMetedCount == preferencesCount:
                    data.metedPreferences[teacher] = True
                else:
                    data.metedPreferences[teacher] = False

        else:
            data.metedPreferences[teacher] = True


#####################################################
####         Algoritmos - Fim
#####################################################


def generateCsv(graph, data):
    schoolClasses = {}
    for v in graph:
        for schedule, color in data.colorsSchedules.items():
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
            if len(week[day]) < len(data.settings):
                scheduleList = data.settings
                for i in range(len(scheduleList)):
                    foundClass = False
                    for cls in week[day]:
                        if cls is not None and scheduleList[i] in cls.schedule:
                            foundClass = True
                    if not foundClass:
                        week[day].insert(i, None)

        matrixPlot = [data.settings]

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

        fig = go.Figure(data=[go.Table(header=dict(values=header), cells=dict(values=matrixPlot))])
        fig.show()


def main():
    data = GlobalData()
    graph = createGraph(data)

    setColorsPreferencesBeforeDsatur(graph, data)
    if dsatur(graph, data.colorsUsed):
        improvement(graph, data)
        # generateCsv(graph, data)
        print(data.metedPreferences)

        if len(data.colorsSchedules) >= len(data.colorsUsed):
            print('Sucesso')
        else:
            print('Opa, mais cores que o ideal :/')
    else:
        print('Erro ao executar o Dsatur')


startTime = time.time()
main()
print("%s segundos - Tempo de execucao" % (time.time() - startTime))
