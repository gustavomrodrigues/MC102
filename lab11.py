'''
Nesse laboratório, foi implementado a lógica de um jogo fictício. Um dia, o reino de Hyrule foi ameaçado por uma terrível força das trevas que estava se espalhando pela masmorra da
cidade. O rei de Hyrule convocou Link, confiando-lhe a missão de explorá-la, derrotar os monstros e recuperar os objetos mágicos que poderiam ajudar a salvar o reino.
Link teve que enfrentar uma maldição que restringia seus movimentos, elas exigia que ele se mova até a última linha, partindo da posição inicial, além de só permitir a movimentação
seguindo as restrições: Mover da esquerda para direita em linhas de número ímpar; Mover da direita para esquerda em linhas de número par.
Ao chegar no limite lateral da masmorra, Link deve ir à linha imediatamente acima da linha atual. Link não pode se movimentar pelas diagonais.  Link encontra objetos valiosos à medida
que Link avança, sempre coletando todos pela frente. Alguns objetos concedem mais vida, fortalecendo sua resistência para enfrentar batalhas difíceis. Outros objetos aumentam seu poder de ataque, 
permitindo que derrotem monstros mais facilmente.
Mais detalhes sobre o funcionamento dos itens coletáveis e do combate com os monstros serão detalhados abaixo junto com um exemplo de entrada e saída.
'''

from dataclasses import dataclass

@dataclass
class Personagem:
    vida: int
    dano: int
    posicao: tuple
    def adquirir_objetos(self, lista_objetos_adquiridos, matriz):
        for objeto in lista_objetos_adquiridos:
            if self.posicao == objeto.posicao:
                if objeto.tipo == 'v':
                    self.vida += int(objeto.status)
                    matriz[objeto.posicao[0]][objeto.posicao[1]] = 'P'
                    print(f'[{objeto.tipo}]Personagem adquiriu o objeto {objeto.nome} com status de {objeto.status}')
                elif objeto.tipo == 'd':
                    self.dano += int(objeto.status)
                    matriz[objeto.posicao[0]][objeto.posicao[1]] = 'P'
                    print(f'[{objeto.tipo}]Personagem adquiriu o objeto {objeto.nome} com status de {objeto.status}')

@dataclass
class Monstro:
    vida: int
    dano: int
    tipo: str
    posicao: tuple

    def achar_posicao_futura(self, linha_max, coluna_max, lista_monstros, matriz):
        for monstro in lista_monstros:
            if monstro.tipo == 'U':
                if monstro.posicao[0] == 0:
                    monstro.posicao = (monstro.posicao[0], monstro.posicao[1])
                elif monstro.posicao[0] - 1 < linha_max:
                    if matriz[monstro.posicao[0]][monstro.posicao[1]] != 'P' and matriz[monstro.posicao[0]][monstro.posicao[1]] != '*' :
                        matriz[monstro.posicao[0]][monstro.posicao[1]] = '.'
                    monstro.posicao = (monstro.posicao[0] - 1, monstro.posicao[1])
            elif monstro.tipo == 'D':
                if monstro.posicao[0] == len(matriz[monstro.posicao[0]]) - 1:
                    monstro.posicao = (monstro.posicao[0], monstro.posicao[1])
                elif monstro.posicao[0] + 1 >= 0:
                    if matriz[monstro.posicao[0]][monstro.posicao[1]] != 'P' and matriz[monstro.posicao[0]][monstro.posicao[1]] != '*' :                        matriz[monstro.posicao[0]][monstro.posicao[1]] = '.'
                    monstro.posicao = (monstro.posicao[0] + 1, monstro.posicao[1])
            elif monstro.tipo == 'R':
                if monstro.posicao[1] + 1 < coluna_max:
                    if matriz[monstro.posicao[0]][monstro.posicao[1]] != 'P' and matriz[monstro.posicao[0]][monstro.posicao[1]] != '*' :                        matriz[monstro.posicao[0]][monstro.posicao[1]] = '.'
                    monstro.posicao = (monstro.posicao[0], monstro.posicao[1] + 1)
            elif monstro.tipo == 'L':
                if monstro.posicao[1] - 1 >= 0:
                    if matriz[monstro.posicao[0]][monstro.posicao[1]] != 'P' and matriz[monstro.posicao[0]][monstro.posicao[1]] != '*' :                        matriz[monstro.posicao[0]][monstro.posicao[1]] = '.'
                    monstro.posicao = (monstro.posicao[0], monstro.posicao[1] - 1)
        return (monstro.posicao[0], monstro.posicao[1])


@dataclass
class Objeto:
    nome: str
    tipo: str
    posicao: list
    status: str 

class Mapa:
    def __init__(self, n_linha, n_coluna, link, posicao_saida):
        ''' Constrói o mapa inicial sem personagens'''
        self.matriz = [["." for _ in range(n_coluna)] for _ in range(n_linha)]
        self.posicao_entrada = None
        self.posicao_saida = posicao_saida
        self.__adiciona_link(link)
        self.condicao_maldicao = True
        self.link_vivo = True
    def __str__(self) -> str:
        return "\n".join([" ".join(linha) for linha in self.matriz])
    
    def __adiciona_link(self, link: Personagem):
        self.link = link
        self.matriz[link.posicao[0]][link.posicao[1]] = 'P'

    def adiciona_monstro(self, monstro: Monstro):
        if self.matriz[monstro.posicao[0]][monstro.posicao[1]] != '*':
            self.matriz[monstro.posicao[0]][monstro.posicao[1]] = monstro.tipo

    def adiciona_objeto(self, objeto: Objeto):
            self.matriz[objeto.posicao[0]][objeto.posicao[1]] = objeto.tipo
    
    def adiciona_saida(self):
        self.matriz[self.posicao_saida[0]][self.posicao_saida[1]] = '*'

    def mover_link(self, posicao):
        ''' Movimenta o link da posição atual para a posição futura '''
        if self.condicao_maldicao:
            posicao[0] = self.link.posicao[0]
            posicao[1] = self.link.posicao[1]
            linha = self.link.posicao[0]
            self.link.posicao = (self.link.posicao[0] + 1, self.link.posicao[1])
            self.matriz[self.link.posicao[0]][self.link.posicao[1]] = 'P'
            self.matriz[self.link.posicao[0] - 1][self.link.posicao[1]] = '.'
            if self.link.posicao[0] == len(self.matriz) - 1:
                self.condicao_maldicao = False 
        else:
            linha = self.link.posicao[0]
            coluna = self.link.posicao[1]
            if linha % 2 == 0:
                if coluna == 0:
                    self.matriz[self.link.posicao[0]][self.link.posicao[1]] = '.'
                    posicao[0] = self.link.posicao[0]
                    posicao[1] = self.link.posicao[1]
                    self.link.posicao = (linha - 1, coluna)
                    self.matriz[self.link.posicao[0]][self.link.posicao[1]] = 'P'

                else:
                    self.matriz[self.link.posicao[0]][self.link.posicao[1]] = '.'
                    self.matriz[linha][coluna - 1] = 'P'
                    posicao[0] = self.link.posicao[0]
                    posicao[1] = self.link.posicao[1]
                    self.link.posicao = (linha, coluna - 1)
            else:
                if coluna == len(self.matriz[linha]) - 1:
                    posicao[0] = self.link.posicao[0]
                    posicao[1] = self.link.posicao[1]
                    self.link.posicao = (linha - 1, coluna)
                else:
                    self.matriz[self.link.posicao[0]][self.link.posicao[1]] = '.'
                    self.matriz[linha][coluna + 1] = 'P'
                    posicao[0] = self.link.posicao[0]
                    posicao[1] = self.link.posicao[1]
                    self.link.posicao = (linha, coluna + 1)

    def mover_monstro(self, lista_monstros):
        ''' Movimento o monstro da posição atual para a posição futura '''
        for monstro in lista_monstros:
            self.matriz[monstro.posicao[0]][monstro.posicao[1]] = monstro.tipo
    
    def resultado_combate(self, lista_monstros_combate, vida_inicial):
        if self.link.vida <= 0:
            self.matriz[self.link.posicao[0]][self.link.posicao[1]] = 'X'
            self.link_vivo = False
        else:
            self.matriz[self.link.posicao[0]][self.link.posicao[1]] = 'P'
        for monstro in lista_monstros_combate:
            if monstro.vida <= 0:
                self.matriz[monstro.posicao[0]][monstro.posicao[1]] = '.'
                self.link.vida = vida_inicial

    def combate(self, lista_monstros_combate, vida_inicial, lista_dano_combate, lista_posicao_combate):
        for monstro in lista_monstros_combate:
            monstro.vida -= self.link.dano
            print(f'O Personagem deu {lista_dano_combate[lista_monstros_combate.index(monstro)]} de dano ao monstro na posicao {lista_posicao_combate[lista_monstros_combate.index(monstro)]} ')
            if monstro.vida >= 0:
                self.link.vida -= monstro.dano
                print(f'O Monstro deu {lista_monstros_combate[lista_monstros_combate.index(monstro)].dano} de dano ao Personagem. Vida restante = {self.link.vida}')
        self.resultado_combate(lista_monstros_combate, vida_inicial)

    
    def tem_objeto(self, lista_objetos, lista_objetos_adquiridos):
        for objeto in lista_objetos:
                if self.link.posicao == objeto.posicao:
                    lista_objetos_adquiridos.append(objeto)
        if len(lista_objetos_adquiridos) > 0:
            return True
        return False

    def tem_combate(self, lista_monstros, lista_monstros_combate, lista_dano_combate, lista_posicao_combate):
        for monstro in lista_monstros:
            if self.link.posicao == monstro.posicao:
                lista_monstros_combate.append(monstro)
                lista_dano_combate.append(self.link.dano)
                lista_posicao_combate.append(monstro.posicao)
        if len(lista_monstros_combate) > 0:
            return True
        
        return False
    
    def checa_objetos(self, lista_objetos, lista_objetos_adquiridos):
        for objeto in lista_objetos:
            if objeto not in lista_objetos_adquiridos:
                if self.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'R' and self.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'L' and self.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'U' and self.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'D':
                    self.matriz[objeto.posicao[0]][objeto.posicao[1]] = objeto.tipo
        
    def checa_monstros(self, lista_monstros):
        for monstro in lista_monstros:
            if monstro.vida > 0:
                if [self.matriz.posicao[0]][self.matriz.posicao[1]] != 'P' and [self.matriz.posicao[0]][self.matriz.posicao[1]] != '*':
                    [self.matriz.posicao[0]][self.matriz.posicao[1]] = monstro.tipo

    
def main():
    vida_dano_link = input().split(' ')
    vida_inicial_link = int(vida_dano_link[0])
    linha_coluna = input().split(' ')
    n_linha = int(linha_coluna[0])
    n_coluna = int(linha_coluna[1])
    posicao_entrada_lista = input().split(',')
    posicao_entrada = (int(posicao_entrada_lista[0]), int(posicao_entrada_lista[1]))
    posicao_saida_lista = input().split(',')
    posicao_saida = (int(posicao_saida_lista[0]), int(posicao_saida_lista[1]))
    link = Personagem(int(vida_dano_link[0]), int(vida_dano_link[1]), posicao_entrada)
    numero_monstros = int(input())
    lista_monstros = []
    mapa = Mapa(n_linha, n_coluna, link, posicao_saida)
    mapa.adiciona_saida()
    for _ in range(numero_monstros):
        info_monstro = input().split(' ')
        posicao_monstro_entrada = info_monstro[3].split(',')
        posicao_monstro = (int(posicao_monstro_entrada[0]), int(posicao_monstro_entrada[1]))
        monstro = Monstro(vida=int(info_monstro[0]), dano=int(info_monstro[1]), tipo=info_monstro[2], posicao=posicao_monstro)
        lista_monstros.append(monstro)
        mapa.adiciona_monstro(monstro)
    numero_objetos = int(input())
    lista_objetos = []       
    for _ in range(numero_objetos):
        info_objeto = input().split(' ')
        posicao_objeto_entrada = info_objeto[2].split(',')
        posicao_objeto = (int(posicao_objeto_entrada[0]), int(posicao_objeto_entrada[1]))
        objeto = Objeto(info_objeto[0], info_objeto[1], posicao_objeto, info_objeto[3])
        lista_objetos.append(objeto)
        mapa.adiciona_objeto(objeto)
        lista_objetos_adquiridos = []
    posicao_anterior = [0,0]
    while link.vida > 0 and link.posicao != posicao_saida:
        print(mapa)
        print()
        lista_monstros_combate = []
        lista_dano_combate = []
        lista_posicao_combate = []
        mapa.mover_link(posicao_anterior)
        if mapa.tem_objeto(lista_objetos, lista_objetos_adquiridos):
            if mapa.matriz[posicao_anterior[0]][posicao_anterior[1]] != 'R' and mapa.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'L' and mapa.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'U' and mapa.matriz[objeto.posicao[0]][objeto.posicao[1]] != 'D':
                mapa.matriz[posicao_anterior[0]][posicao_anterior[1]] = '.'
            link.adquirir_objetos(lista_objetos_adquiridos, mapa.matriz)
        monstro.achar_posicao_futura(n_linha, n_coluna, lista_monstros, mapa.matriz)
        mapa.mover_monstro(lista_monstros)
        if mapa.tem_combate(lista_monstros, lista_monstros_combate, lista_dano_combate, lista_posicao_combate):
            mapa.combate(lista_monstros_combate, vida_inicial_link, lista_dano_combate, lista_posicao_combate)
            mapa.checa_monstros(lista_monstros)
        mapa.checa_objetos(lista_objetos, lista_objetos_adquiridos)
        if link.vida == 0:
            print(mapa)
            print()
            break
        mapa.adiciona_saida()
    if link.posicao == posicao_saida:
        mapa.matriz[posicao_saida[0]][posicao_saida[1]] = 'P'
        print(mapa)
        print()
        print('Chegou ao fim!')
      
if __name__ == '__main__':
    main()

'''
Cada item coletável pode ser um dos dois tipos disponíveis:
- v (vida): adiciona um certo valor à vida atual de Link. Este valor pode ser tanto positivo ou negativo, sendo possível que ele morra após coletar algum item.
- d (dano): adiciona um certo valor ao dano atual de Link. Pode ser positivo ou negativo.
Em caso de valores menores que 1 (um), o dano mínimo permitido deve ser fixado em 1.
Assim como os objetos, cada monstro possui um tipo específico que determinava o seu padrão de movimentação. Os tipos disponíveis são:
- U: move para uma posição imediatamente acima da atual
- D: move para uma posição imediatamente abaixo da atual
- L: move para uma posição à esquerda da atual
- R: move para uma posição à direita da atual
Caso a próxima posição do monstro, conforme o seu tipo de movimentação, seja para uma posição fora da matriz, o mesmo deve ficar parado.
Link entra em combate com um monstro quando ambos se encontram na masmorra (ocupam a mesma posição). No combate, ele sempre ataca primeiro e recebe o dano em seguida (caso o
monstro sobreviva). O turno de combate acontece uma vez naquela posição específica, ou seja, caso os dois envolvidos sobrevivam ao ataque, ambos seguem sua movimentação
normalmente na próxima rodada. Caso Link ocupe a mesma posição que dois ou mais monstros, a luta acontece contra todos os inimigos, um de cada vez. Se a próxima
movimentação de Link coincidir com a próxima posição do monstro, ambos se enfrentam novamente. Em casos que a posição atual coincide com a posição de um ou mais monstros e um ou mais
objetos, adote que Link primeiro coleta cada objeto e depois muda para o ato de combate. Por fim, o objetivo de Link é atingir uma posição específica no mapa que vai levá-lo até a saída
masmorra, livrando assim a cidade de todo o perigo que lá havia por um tempo.

A entrada do programa é constituída pelas seguintes informações, em ordem:
- Dois inteiros Vp e Dp, indicando a vida e o dano inicial do Link, respectivamente;
- Dois inteiros N e M, indicando o número de linhas e colunas do mapa, respectivamente;
- Dois inteiros I indicando a posição inicial do personagem na masmorra;
- Em seguida, recebe-se dois inteiros F , indicando a posição de saída da masmorra;
- Um inteiro Q indicando o número de monstros no mapa; m
- Q linhas contendo 5 informações sobre cada monstro: vida, ataque, tipo e posição inicial do monstro;
- Um inteiro B indicando o número de objetos no mapa;
- B linhas contendo 5 informações sobre cada objeto: nome, tipo, posição e status do objeto. O status pode ser entendido como o valor a ser somado à vida ou ao
ataque de Link, dependendo do tipo do objeto. Este valor pode ser positivo ou negativo.

Saída
Deve-se imprimir o estado do mapa ao final da movimentação do personagem e dos monstros e de qualquer resolução de combate, assim como coleta de itens. Assuma que Link anda
sempre primeiro que os monstros. A posição atual do personagem deve ser indicada pela letra P, posição de chegada pelo símbolo *, os monstros pelo seu respectivo tipo (U, D, R, L) ,
assim como os objetos (v ou d). Se o personagem morre após um certo combate ou após a obtenção de algum objeto, deve-se imprimir X no lugar de P e automaticamente a jornada deve
parar. Os espaços das masmorras sem nenhum personagem, objeto, monstro, ou que seja posição de chegada deve ser mostrado como '.' (ponto final).

Exemplo

Entrada
5 10
4 4
0,1
0,3
3
100 5 U 1,0
110 5 R 2,0
100 5 R 3,0
2
joia d 1,2 -1
chocolate v 2,2 5

Saída

. P . *
U . d .
R . v .
R . . .

U . . *
. P d .
. R v .
. R . .

U . . *
. . d .
. P R .
. . R .

U . . *
. . d .
. . v R
. P . R

U . . *
. . d .
. . v R
. . P R
O Personagem deu 10 de dano ao monstro na posicao (3, 3)
O Monstro deu 5 de dano ao Personagem. Vida restante = 0

U . . *
. . d .
. . v R
. . . X
'''
