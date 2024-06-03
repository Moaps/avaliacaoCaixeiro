import copy as cp
import random as rd
from caixeiro_viajante import Caixeiro


class SubidaDeEncosta:
    def __init__(self, num_cidades, matriz_distancias):
        self.num_cidades = num_cidades
        self.matriz_distancias = matriz_distancias

    # Função para gerar sucessores para a subida de encosta (melhor vizinho)
    def gerar_melhor_sucessor(self, solucao_atual, caixeiro):
        indice_fixo = rd.randrange(self.num_cidades)
        melhor_valor = float('inf')
        melhor_solucao = None

        for i in range(self.num_cidades):
            if i != indice_fixo:
                nova_solucao = cp.deepcopy(solucao_atual)
                nova_solucao[i], nova_solucao[indice_fixo] = nova_solucao[indice_fixo], nova_solucao[i]
                valor_sucessor = caixeiro.avaliar_solucao(nova_solucao)
                if valor_sucessor < melhor_valor:
                    melhor_valor = valor_sucessor
                    melhor_solucao = cp.deepcopy(nova_solucao)

        return melhor_solucao, melhor_valor

    # Método de busca local: Subida de Encosta
    def subida_encosta(self, solucao_inicial, valor_inicial, caixeiro):
        solucao_atual = cp.deepcopy(solucao_inicial)
        valor_atual = valor_inicial

        while True:
            nova_solucao, novo_valor = self.gerar_melhor_sucessor(solucao_atual, caixeiro)
            if novo_valor >= valor_atual:
                return solucao_atual, valor_atual
            solucao_atual = cp.deepcopy(nova_solucao)
            valor_atual = novo_valor