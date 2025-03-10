'''
Nesse laboratório o objetivo é descriptografar uma mensagem. Na entrada é informada a operação a ser feita para cálcular a chave de criptografia,
os caracteres ou marcadores de tipo para a busca, o número de linhas da mensagem e a mensagem em si
'''

def possibilidade_operandos(operando, codigo_orig):
    ''' Avaliando qual a forma do operando '''
    vogal = 'aeiou'
    consoante = 'bcdfghjklmnpqrstvxwyzBCDFGHJKLMNPQRSTVXWYZ'
    numero = '0123456789'
    if operando == 'vogal':
        for i in range(len(codigo_orig)):
            if codigo_orig[i] in vogal:
                operando = codigo_orig[i]
                break
    elif operando == 'consoante':
        for i in range(len(consoante)):
            if codigo_orig[i] in consoante:
                operando = codigo_orig[i]
                break
    elif operando == 'numero':
        for i in range(len(numero)):
            if codigo_orig[i] in numero:
                operando = codigo_orig[i]
                break
    return operando


def posicao_operandos(operando1, operando2, codigo_orig):
    ''' Definindo a posição dos operandos '''
    pos_operando1 = codigo_orig.find(operando1)
    pos_operando2 = codigo_orig[pos_operando1:].find(operando2) + pos_operando1
    return pos_operando1, pos_operando2


def definindo_chave(operador, pos_operando1, pos_operando2, codigo_orig):
    ''' Definindo a chave '''
    if operador == '+':
        chave = pos_operando1 + pos_operando2
    elif operador == '-':
        chave = pos_operando1 - pos_operando2
    elif operador == '*':
        chave = pos_operando1 * pos_operando2

    return chave


def input_codigo(n_linhas):
    ''' Realizando o input'''
    i = 0
    lista_partes_codigo = []
    while i < n_linhas:
        parte_codigo = input()
        lista_partes_codigo.append(parte_codigo)
        i += 1

    return lista_partes_codigo


def junta_partes_codigo(input_codigo):
    ''' Juntando as linhas diferentes do código '''
    codigo_orig = ''
    for i in range(len(input_codigo)):
        codigo_orig += input_codigo[i]

    return codigo_orig


def define_tamanho_string(entrada):
    ''' Armazenando o tamanho das linhas '''
    lista_tamanho_strings = []
    for i in range(len(entrada)):
        lista_tamanho_strings.append(len(entrada[i]))
    return lista_tamanho_strings


def descriptografando(chave, codigo_orig):
    ''' Realizando a descriptografia do código '''
    novo_codigo = ""
    for i in range(len(codigo_orig)):
        nova_posicao = (((ord(codigo_orig[i]) + chave) - 32) % 95) + 32
        novo_elemento = chr(nova_posicao)
        novo_codigo += novo_elemento

    return novo_codigo


def saida(novo_codigo, lista_tamanho_strings):
    ''' Saída '''
    codigo_correto = ""
    j = 0
    z = 0
    i = 0
    while i < (len(lista_tamanho_strings)):
        codigo_correto += novo_codigo[j:j + lista_tamanho_strings[i]] + '\n'
        j += lista_tamanho_strings[z]
        z += 1
        i += 1
    return codigo_correto


def main():
    operador = input()
    operando1 = input()
    operando2 = input()
    n_linhas = int(input())
    entrada = input_codigo(n_linhas)
    codigo_orig = junta_partes_codigo(entrada)
    operando_1 = possibilidade_operandos(operando1, codigo_orig)
    operando_2 = possibilidade_operandos(operando2, codigo_orig)
    (x, y) = posicao_operandos(operando_1, operando_2, codigo_orig)
    chave = definindo_chave(operador, x, y, codigo_orig)
    lista_tamanho_string = define_tamanho_string(entrada)
    novo_codigo = descriptografando(chave, codigo_orig)
    codigo_descriptografado = saida(novo_codigo, lista_tamanho_string)

    print(chave)
    print(codigo_descriptografado)


if __name__ == '__main__':
    main()

'''
Exemplo

Entrada
+
f
Z
1
J\vmfZ\v\jkXvc\e[fv`jjf#vfvi\jlckX[fv\jkXvZfii\kfw

Saída
9
Se voce esta lendo isso, o resultado esta correto!
'''
