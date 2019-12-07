import sys
import pandas as pd
import math
import time

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
                        if j.theme == vertex.theme and j.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                            if scheduleConfig.index(j.schedule.split('-')[1]) - 2 == scheduleConfig.index(colorKey.split('-')[1]):
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
                        if j.theme == vertex.theme and j.schoolClass == vertex.schoolClass and colorKey.split('-')[0] in v.schedule:
                            if scheduleConfig.index(j.schedule.split('-')[1]) + 2 == scheduleConfig.index(colorKey.split('-')[1]):
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


def getBiggerSaturVertexId(graph):
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


colorsTest = []


def toColor(vertex, graph, schedulesConfig):
    # for c in colors.values():
    #     if c not in vertex.restrictionsColors:
    #         vertex.setColor(c)
    #         break

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
                if c not in colorsTest:
                    colorsTest.append(c)

        else:
            valid = False

        c += 1


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
    colorsTest.sort()
    print(colorsTest)
    reducedColors = []
    while reducedColors != colorsTest:
        reducedColors = colorsTest
        colorsTest = []
        for c in reducedColors:
            for v in graph:
                if v.color == c:
                    i = 1
                    colorful = False
                    while i in colors.values() and not colorful:
                        if i not in v.restrictionsColors and i != v.color:

                            valid = True

                            for adj in v.adjacents:
                                if adj.color == i:
                                    valid = False
                                    break

                            if valid:
                                # aqui seta a cor direto ao inves de usar a funcao setColor pois dsatur nao sera mais usado
                                v.color = i
                                colorful = True

                            if v.color not in colorsTest:
                                colorsTest.append(v.color)
                        i += 1
    colorsTest.sort()
    print(colorsTest)
    colorfulValid = []
    colorfulInvalid = []
    for v in graph:
        if v.color in colors.values():
            colorfulValid.append(v)
        else:
            colorfulInvalid.append(v)

    print('Quantidade de cores: ' + str(len(colorsTest)))

    for schedule, c in colors.items():
        print('Dia/Horario: ' + schedule)
        for v in colorfulValid:
            if v.color == c:
                print('Turma: ', v.schoolClass, ' - ', v.teacher, ' - Materia', v.theme)

    print('Sem horario: ')
    for v in colorfulInvalid:
        if v.color == c:
            print('Turma: ', v.schoolClass, ' - ', v.teacher, ' - Materia', v.theme)

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

    file = open('out.csv', 'w')

    for sc, listSC in schoolClasses.items():
        listSC.sort(key=lambda s: s.color)

        file.write('\n\nTurma: ' + str(sc) + ',')
        segunda = []
        terca = []
        quarta = []
        quinta = []
        sexta = []
        week = [segunda, terca, quarta, quinta, sexta]
        for scItem in listSC:
            if 'Segunda' in scItem.schedule:
                segunda.append(scItem)
            elif 'Terça' in scItem.schedule:
                terca.append(scItem)
            elif 'Quarta' in scItem.schedule:
                quarta.append(scItem)
            elif 'Quinta' in scItem.schedule:
                quinta.append(scItem)
            else:
                sexta.append(scItem)

        for day in week:
            for scItem in day:
                scItem.schedule = time.strptime(
                    scItem.schedule.split('-')[1], '%H:%M')
            day.sort(key=lambda s: s.schedule)

        for horario in schedulesConfig():
            file.write(horario + ',')
        file.write('\nSegunda,')
        for aula in segunda:
            file.write(aula.teacher + ' - Matéria: ' + aula.theme + ',')
        file.write('\nTerça,')
        for aula in terca:
            file.write(aula.teacher + ' - Matéria: ' + aula.theme + ',')
        file.write('\nQuarta,')
        for aula in quarta:
            file.write(aula.teacher + ' - Matéria: ' + aula.theme + ',')
        file.write('\nQuinta,')
        for aula in quinta:
            file.write(aula.teacher + ' - Matéria: ' + aula.theme + ',')
        file.write('\nSexta,')
        for aula in sexta:
            file.write(aula.teacher + ' - Matéria: ' + aula.theme + ',')

else:
    print('Que merda!')

print("%s segundos - Tempo de execucao" % (time.time() - startTime))
