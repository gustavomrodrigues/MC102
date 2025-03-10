from typing import List, Tuple, Any

'''
Nesse laboratório foi implementado um código que realiza operações com vetores que podem
ou não ter tamanhos diferentes. Como entrada é fornecido um vetor inicial e um conjunto
operações a serem feitas
'''
def converte_vetor_int(vetor1: List[str]) -> List[Any]:
    ''' Converte os elementos dos vetores em int '''
    i = 0
    resultado: List[Any] = vetor1
    while i < len(vetor1):
        resultado[i] = int(vetor1[i])
        i += 1
    return resultado


def add_n(v1: List[int], v2: List[int], n: int) -> Tuple[List[int], List[int]]:
    ''' Adiciona um número ao final do vetor '''
    if len(v1) > len(v2):
        i = len(v1) - len(v2)
        while i != 0:
            v2.append(n)
            i -= 1
    elif len(v2) > len(v1):
        i = len(v2) - len(v1)
        while i != 0:
            v1.append(n)
            i -= 1
    return v1, v2


def soma_vetores(vetor1: List[int], vetor2: List[int]) -> List[int]:
    ''' Soma os elementos dos vetores entre si '''
    add_n(vetor1, vetor2, 0)
    for i in range(len(vetor1)):
        vetor1[i] = vetor1[i] + vetor2[i]
    return vetor1


def subtrai_vetores(vetor1: List[int], vetor2: List[int]) -> List[int]:
    ''' Subtrai os elementos dos vetores entre si '''
    add_n(vetor1, vetor2, 0)
    for i in range(len(vetor1)):
        vetor1[i] = vetor1[i] - vetor2[i]
    return vetor1


def multiplica_vetores(vetor1: List[int], vetor2: List[int]) -> List[int]:
    ''' Multiplica os elementos dos vetores entre si '''
    add_n(vetor1, vetor2, 1)
    for i in range(len(vetor1)):
        vetor1[i] = vetor1[i] * vetor2[i]
    return vetor1


def divide_vetores(vetor1: List[int], vetor2: List[int]) -> List[int]:
    ''' Divide os elementos dos vetores entre si '''
    if len(vetor1) > len(vetor2):
        i = len(vetor1) - len(vetor2)
        while i != 0:
            vetor2.append(1)
            i -= 1
    elif len(vetor2) > len(vetor1):
        i = len(vetor2) - len(vetor1)
        while i != 0:
            vetor1.append(0)
            i -= 1
    for i in range(len(vetor1)):
        vetor1[i] = vetor1[i] // vetor2[i]
    return vetor1


def multiplicacao_escalar(vetor1: List[int], escalar: int) -> List[int]:
    ''' Multiplica os elementos dos vetores por um escalar '''
    resultado = vetor1
    for i in range(len(vetor1)):
        resultado[i] = vetor1[i] * escalar
    return resultado


def n_duplicacao(vetor1: List[int], n: int) -> List[int]:
    ''' Repete o vetor inicial n vezes '''
    lista_duplicada_n_vezes = []
    while n != 0:
        for i in range(len(vetor1)):
            lista_duplicada_n_vezes.append(vetor1[i])
        n -= 1
    return lista_duplicada_n_vezes


def soma_elementos(vetor1: List[int]) -> int:
    ''' Soma os elementos de um vetor '''
    soma = 0
    i = 0
    while i < len(vetor1):
        soma = soma + vetor1[i]
        i += 1
    resultado = soma
    return resultado


def produto_interno(vetor1: List[int], vetor2: List[int]) -> int:
    ''' Multiplica cada elemento dos vetores e depois soma o resultado '''
    add_n(vetor1, vetor2, 1)
    produto_interno = 0
    i = 0
    while i < len(vetor1):
        produto_interno = produto_interno + (vetor1[i] * vetor2[i])
        i += 1
    resultado = produto_interno
    return resultado


def multiplica_todos(vetor1: List[int], vetor2: List[int]) -> List[int]:
    ''' Multiplica os elementos do 1º vetor pelos do 2º vetor e soma '''
    resultado = vetor1
    for i in range(len(vetor1)):
        resultado[i] = vetor1[i] * soma_elementos(vetor2)
    return resultado


def correlacao_cruzada(vetor1: List[int], mascara: List[int]) -> List[int]:
    ''' Um vetor menor caminha pelo vetor calculando um produto interno '''
    vetor_corrente = []
    vetor_resultado = []
    h = 0
    while h < len(vetor1):
        vetor_corrente.append(0)
        h += 1
    for i in range(len(vetor1) - len(mascara) + 1):
        for j in range(len(mascara)):
            vetor_corrente[i] = vetor_corrente[i] + vetor1[i+j] * mascara[j]
        vetor_resultado.append(vetor_corrente[i])
    return vetor_resultado


def main() -> None:
    ''' Função main '''
    vetor1 = converte_vetor_int(input().split(','))
    comando = str(input())
    if comando == 'fim':
        exit()
    else:
        while (comando != 'fim'):
            if comando == 'soma_vetores':
                vetor2 = converte_vetor_int(input().split(','))
                print(soma_vetores(vetor1, vetor2))
            elif comando == 'subtrai_vetores':
                vetor2 = converte_vetor_int(input().split(','))
                vetor1 = subtrai_vetores(vetor1, vetor2)
                print(vetor1)
            elif comando == 'multiplica_vetores':
                vetor2 = converte_vetor_int(input().split(','))
                vetor1 = multiplica_vetores(vetor1, vetor2)
                print(vetor1)
            elif comando == 'divide_vetores':
                vetor2 = converte_vetor_int(input().split(','))
                vetor1 = divide_vetores(vetor1, vetor2)
                print(vetor1)
            elif comando == 'multiplicacao_escalar':
                escalar = int(input())
                vetor1 = multiplicacao_escalar(vetor1, escalar)
                print(vetor1)
            elif comando == 'n_duplicacao':
                n = int(input())
                vetor1 = n_duplicacao(vetor1, n)
                print(vetor1)
            elif comando == 'soma_elementos':
                vetor1 = [soma_elementos(vetor1)]
                print(vetor1)
            elif comando == 'produto_interno':
                vetor2 = converte_vetor_int(input().split(','))
                vetor1 = [produto_interno(vetor1, vetor2)]
                print(vetor1)
            elif comando == 'multiplica_todos':
                vetor2 = converte_vetor_int(input().split(','))
                vetor1 = multiplica_todos(vetor1, vetor2)
                print(vetor1)
            elif comando == 'correlacao_cruzada':
                mascara = converte_vetor_int(input().split(','))
                vetor1 = correlacao_cruzada(vetor1, mascara)
                print(vetor1)
            comando = str(input())


if __name__ == '__main__':
    main()

'''
Exemplo

Entrada
2,-3,4
soma_vetores
-1,2,3,4
subtrai_vetores
-1,2,3
multiplica_vetores
1,0,-2
divide_vetores
-1,-1,3,3,1
fim

Saída
[1, -1, 7, 4]
[2, -3, 4, 4]
[2, 0, -8, 4]
[-2, 0, -3, 1, 0]
'''
