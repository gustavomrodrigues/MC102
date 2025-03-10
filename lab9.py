'''
Nesse laboratório é feita uma lógica para um robô aspirador limpar um cômodo. Esse cômodo é representado por uma matriz, e o robô deve limpar todo o cômodo sem deixar nenhuma sujeira.
O robô tem uma visão de apenas uma posição adjacente (para os lados, para cima e para baixo). O robô possui 4 modos, os quais serão detalhados junto com um exemplo de entrada e saída abaixo.
'''

def mover_robo(matriz_inicial, posicao_atual, posicao_futura):
    ''' Movimenta o robô da posição atual para a posição futura'''
    matriz_inicial[posicao_atual[0]][posicao_atual[1]] = '.'
    matriz_inicial[posicao_futura[0]][posicao_futura[1]] = 'r'
    print()
    imprimir_matriz(matriz_inicial)


def imprimir_matriz(matriz_inicial):
    ''' Imprime a matriz '''
    for linha in matriz_inicial:
        print(' '.join(linha))
     

def escaneamento(matriz_inicial):
    ''' Escaneia o cômodo do robô '''
    for linha in range(len(matriz_inicial)):
        if linha % 2 == 0:
            coluna = 0
            if linha != 0:
                mover_robo(matriz_inicial, (linha - 1, coluna), (linha, coluna))
            while coluna < len(matriz_inicial[linha]) - 1:
                if matriz_inicial[linha][coluna + 1] == '.':
                    posicao_robo = (linha, coluna)
                    posicao_atual = modo_limpeza(matriz_inicial, posicao_robo)
                    retornar_escaneamento(matriz_inicial, posicao_robo, posicao_atual)
                    mover_robo(matriz_inicial, posicao_robo, (linha, coluna + 1))
                elif matriz_inicial[linha][coluna + 1] == 'o':
                    mover_robo(matriz_inicial, (linha, coluna), (linha, coluna + 1))
                coluna += 1
        else:
            coluna = len(matriz_inicial[0]) - 1
            mover_robo(matriz_inicial, (linha - 1, coluna), (linha, coluna))
            while coluna > 0:
                if matriz_inicial[linha][coluna - 1] == '.':
                    posicao_robo = (linha, coluna)
                    posicao_atual = modo_limpeza(matriz_inicial, posicao_robo)
                    retornar_escaneamento(matriz_inicial, posicao_robo, posicao_atual)
                    mover_robo(matriz_inicial, posicao_robo, (linha, coluna - 1))
                    posicao_robo = (linha, coluna - 1)
                elif matriz_inicial[linha][coluna - 1] == 'o':
                    mover_robo(matriz_inicial, (linha, coluna), (linha, coluna - 1))
                coluna -= 1           
            if linha == len(matriz_inicial) - 1:
                while coluna != len(matriz_inicial[0]) - 1:
                    mover_robo(matriz_inicial, (linha, coluna), (linha, coluna + 1))
                    coluna += 1


def buscando_sujeira(matriz_inicial, posicao_robo):
        ''' Busca sujeira nas 4 posições ao seu redor '''
        linha, coluna = posicao_robo
        posicao_futura = None
        if coluna - 1 >= 0 and matriz_inicial[linha][coluna - 1] == 'o':
            posicao_futura = (linha, coluna - 1)
        elif linha - 1 >= 0 and matriz_inicial[linha - 1][coluna] == 'o':
            posicao_futura = (linha - 1, coluna)
        elif coluna + 1 < len(matriz_inicial[linha]) and matriz_inicial[linha][coluna + 1] == 'o':
            posicao_futura = (linha, coluna + 1)
        elif linha + 1 < len(matriz_inicial) and matriz_inicial[linha + 1][coluna] == 'o':
            posicao_futura = (linha + 1, coluna)
        return posicao_futura


def modo_limpeza(matriz_inicial, posicao_robo):
        ''' Entra no modo limpeza e sai do modo quando não há mais sujeira. Retorna a posição final'''
        posicao_atual = posicao_robo
        posicao_futura = buscando_sujeira(matriz_inicial, posicao_atual)
        while posicao_futura != None:
            mover_robo(matriz_inicial, posicao_atual, posicao_futura)
            posicao_atual = posicao_futura
            posicao_futura = buscando_sujeira(matriz_inicial, posicao_atual)
        return posicao_atual


def retornar_escaneamento(matriz_inicial, posicao_objetivo, posicao_inicial):
    ''' Retorna o robô à sua posição objetivo, dado que ele está na posição inicial'''
    while posicao_inicial != posicao_objetivo:
        if posicao_inicial[1] > posicao_objetivo[1]:
            posicao_futura = (posicao_inicial[0], posicao_inicial[1] - 1)
        elif posicao_inicial[1] < posicao_objetivo[1]:
            posicao_futura = (posicao_inicial[0], posicao_inicial[1] + 1)
        else:
            if posicao_inicial[0] > posicao_objetivo[0]:
                posicao_futura = (posicao_inicial[0] - 1, posicao_inicial[1])
            elif posicao_inicial[0] < posicao_objetivo[0]:
                posicao_futura = (posicao_inicial[0] + 1, posicao_inicial[1])
        mover_robo(matriz_inicial, posicao_inicial, posicao_futura)
        posicao_inicial = posicao_futura
        posicao_inicial = modo_limpeza(matriz_inicial, posicao_inicial)

def main():
    matriz_inicial = []
    n_linhas = int(input())
    for _ in range(n_linhas):
        linha = []
        copia_linha = linha.copy()
        dados = input().split()
        for j in range(len(dados)):
            copia_linha.append(dados[j])
        matriz_inicial.append(copia_linha)
    imprimir_matriz(matriz_inicial)
    escaneamento(matriz_inicial)


if __name__ == "__main__":
    main()
  
'''
MODOS DE FUNCIONAMENTO DO ROBÔ
Escaneamento do ambiente: a partir da posição atual o seu robô deve escanear
o ambiente buscando por sujeira seguindo linha por linha. Se estiver numa linha
par (0, 2, 4, ...), deve realizar o escaneamento da esquerda para a direita, e se
estiver numa linha ímpar (1, 3, 5, ...), deve realizar o escaneamento para da direita
para a esquerda. O seu robô deve andar na direção correta até encontrar uma
parede, descer para linha de baixo e continuar a busca seguindo na direção oposta.
Se durante o processo de escaneamento for encontrado sujeira na adjacência
do robô, ele deve então trocar para o modo “limpando”.
● Limpando: Nesse modo o robô está na posição (i, j), o que significa que essa
posição acabou de ser limpa (independentemente se estava suja ou não). Ele
continua a limpeza olhando para as posições a esquerda, cima, direita e baixo,
nesta ordem. Se alguma delas estiver suja, ele deve ir para a posição onde
encontrou a primeira sujeira para limpá-la. Após realizar essa limpeza o robô possui
três possíveis ações, dependendo do estado do ambiente:
1) A sujeira que acabou de ser limpa está na posição que seria a próxima posição no
escaneamento do ambiente, o robô então deve retornar ao modo “escaneamento do
ambiente” e continuar o escaneamento a partir dessa posição.
2) A sujeira que foi limpa não está no caminho de escaneamento do robô e possui
mais sujeira nas adjacências (uma posição à esquerda, cima, direita ou baixo) do
robô, nesse caso o robô deve continuar no modo “limpando” e proceder como
descrito acima.
3) O robô não está na próxima posição do escaneamento e não tem mais nenhuma
sujeira nas adjacências dele, nesse caso o robô deve então trocar para o modo
“retornar ao escaneamento do ambiente”.
● Retornar ao escaneamento do ambiente: para retornar ao modo “escaneamento
do ambiente”, após finalizar o modo “limpando”, seu robô deve seguir na linha
até a coluna onde parou a busca e depois seguir na coluna até a posição onde
parou o escaneamento, quando chegar na posição onde parou o escaneamento,

deve trocar para o modo “escaneamento do ambiente”. Se durante o retorno
encontrar sujeira ao redor (uma posição à esquerda, cima, direita ou baixo), então
o robô deve trocar para o modo “limpeza”.
Exemplo: sua busca parou na linha 1 e coluna 3, mas seu robô encontrou sujeira e
após limpar todo o setor parou na linha 4 e coluna 5. Então você deve primeiramente
navegar até a coluna 3 e depois subir até a linha 1.
● Finalizar limpeza: o robô deve finalizar a limpeza no canto inferior direito (última
linha da última coluna). Caso ao fim do escaneamento o robô já esteja na posição
correta, o robô deve então ser desligado. Caso no fim do escaneamento o robô
esteja na primeira coluna da última linha, o robô deve navegar para direita em
direção à última coluna. Ao chegar na posição correta, deve desligar o robô. Assim
que o robô é desligado, a limpeza do ambiente é finalizada.

Exemplo
Entrada
3
r . .
. o o
. . .

Saída
r . .
. o o
. . .

. r .
. o o
. . .

. . .
. r o
. . .

. . .
. . r
. . .

. . .
. r .
. . .

. r .
. . .
. . .

. . r
. . .
. . .

. . .
. . r
. . .

. . .
. r .
. . .

. . .
r . .
. . .

. . .
. . .
r . .

. . .
. . .
. r .

. . .
. . .
. . r

'''
    
