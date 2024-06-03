import numpy as np
import random as rd


class Caixeiro:
    def __init__(self, num_cidades):
        self.num_cidades = num_cidades
        self.matriz_distancias = self.gerar_problema()

    # Método para gerar um problema (matriz de distâncias)
    def gerar_problema(self):
        matriz_distancias = np.random.randint(5, 25, (self.num_cidades, self.num_cidades))
        for i in range(self.num_cidades):
            matriz_distancias[i][i] = 0
        return matriz_distancias

    # Método para gerar uma solução inicial
    def gerar_solucao_inicial(self):
        solucao = list(range(self.num_cidades))
        rd.shuffle(solucao)
        return solucao

    # Método para avaliar uma solução
    def avaliar_solucao(self, solucao):
        custo_total = 0
        for i in range(self.num_cidades - 1):
            custo_total += self.matriz_distancias[solucao[i]][solucao[i + 1]]
        custo_total += self.matriz_distancias[solucao[-1]][solucao[0]]
        return custo_total