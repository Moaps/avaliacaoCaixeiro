import copy as cp
import random as rd
from caixeiro_viajante import Caixeiro


class SubidaDeEncostaAlterada:
    def __init__(self, num_cidades, matriz_distancias):
        self.num_cidades = num_cidades
        self.matriz_distancias = matriz_distancias

    # Função para gerar sucessores (vizinho aleatório) para a subida de encosta alterada
    def gerar_sucessor_randomico(self, solucao_atual, caixeiro):
        indice1 = rd.randrange(self.num_cidades)
        indice2 = indice1
        while indice1 == indice2:
            indice2 = rd.randrange(self.num_cidades)

        nova_solucao = cp.deepcopy(solucao_atual)
        nova_solucao[indice1], nova_solucao[indice2] = nova_solucao[indice2], nova_solucao[indice1]
        valor_sucessor = caixeiro.avaliar_solucao(nova_solucao)

        return nova_solucao, valor_sucessor

    # Método de busca local: Subida de Encosta Alterada
    def subida_encosta_alterada(self, solucao_inicial, valor_inicial, caixeiro, tmax):
        solucao_atual = cp.deepcopy(solucao_inicial)
        valor_atual = valor_inicial
        contador_tempo = 1

        while True:
            nova_solucao, novo_valor = self.gerar_sucessor_randomico(solucao_atual, caixeiro)
            if novo_valor >= valor_atual:
                if contador_tempo > tmax:
                    return solucao_atual, valor_atual
                else:
                    contador_tempo += 1
            else:
                solucao_atual = cp.deepcopy(nova_solucao)
                valor_atual = novo_valor
                contador_tempo = 1