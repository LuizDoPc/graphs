#!/usr/bin/env python
# coding: utf-8

# In[600]:


import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import time
import sys


# Classe que guarda os IDs dos vértices do grafo e as arestas, há também a possibilidade de criar um grafo direcional,
# o qual não é o caso deste problema
class Graph:

    def __init__(self, graph_dict={}):
        if (isinstance(graph_dict, Graph)):
            self.__graph_dict = copy.deepcopy(graph_dict.__graph_dict)
        else:
            self.__graph_dict = graph_dict

    def vertices(self):
        return list(self.__graph_dict.keys())

    def edges(self):
        return self.__generate_edges()

    def add_vertex(self, vertex): # Adiciona um vértice ao grafo caso ele já não exista
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge, bidirectional=True): # Desempacota uma aresta e adiciona os vértices que a compõe ao grafo e chama a função 
        (vertex1, vertex2, cost) = edge            # que insere um arco, caso seja um grafo não-direcionado, insere a volta
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        self.__add_edge_no_repetition(vertex1, vertex2, cost)
        if bidirectional:
            self.__add_edge_no_repetition(vertex2, vertex1, cost)

    def direct_cost(self, vertex1, vertex2): # Retorna o valor do peso que liga as duas arestas, caso ela não exista, retorna infinito
        list_v1 = self.__graph_dict[vertex1]
        for (v, cost) in list_v1:
            if v == vertex2:
                return cost
        else:
            return float('inf')

    def __add_edge_no_repetition(self, v1, v2, cost): # Insere uma aresta no grafo (não aceita arestas paralelas)
        list_v1 = self.__graph_dict[v1]
        for i, (v, _) in enumerate(list_v1):
            if v == v2:
                list_v1[i] = (v2, cost)
                break
        else:
            list_v1.append((v2, cost))

    def __generate_edges(self): # Monta e retorna as arestas em tuplas do grafo
        edges = []
        for vertex in self.__graph_dict:
            for (neighbour, cost) in self.__graph_dict[vertex]:
                if (neighbour, vertex) not in edges:
                    edges.append((vertex, neighbour, cost))
        return edges

    def __str__(self):
        return 'Vertices: {0}\nEdges: {1}'.format(sorted(self.vertices()), sorted(self.edges()))
