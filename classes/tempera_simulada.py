import copy as cp
import random as rd
import math as ma
from caixeiro_viajante import Caixeiro


class TemperaSimulada:
    def __init__(self, num_cidades, matriz_distancias):
        self.num_cidades = num_cidades
        self.matriz_distancias = matriz_distancias

    # Função para gerar sucessores para a têmpera simulada
    def gerar_sucessor_tempera(self, atual, caixeiro):
        indice1 = rd.randrange(self.num_cidades)
        indice2 = indice1
        while indice1 == indice2:
            indice2 = rd.randrange(self.num_cidades)

        sucessor = cp.deepcopy(atual)
        sucessor[indice1], sucessor[indice2] = sucessor[indice2], sucessor[indice1]
        custo_sucessor = caixeiro.avaliar_solucao(sucessor)

        return sucessor, custo_sucessor

    # Método de busca local: Têmpera Simulada
    def tempera(self, solucao_inicial, custo_inicial, caixeiro, temperatura_inicial, temperatura_final,
                fator_reducao_temperatura):
        atual = cp.deepcopy(solucao_inicial)
        melhor = cp.deepcopy(solucao_inicial)
        custo_atual = custo_inicial
        melhor_custo = custo_inicial
        temperatura = temperatura_inicial
        while temperatura > temperatura_final:
            novo, custo_novo = self.gerar_sucessor_tempera(atual, caixeiro)
            diferenca_custo = custo_novo - custo_atual
            if diferenca_custo < 0:
                atual = cp.deepcopy(novo)
                custo_atual = custo_novo
                melhor = cp.deepcopy(novo)
                melhor_custo = custo_novo
            else:
                aleatorio = rd.uniform(0, 1)
                if ma.exp(-diferenca_custo / temperatura) > aleatorio:
                    atual = cp.deepcopy(novo)
                    custo_atual = custo_novo
            temperatura *= fator_reducao_temperatura
        return melhor, melhor_custo