'''
Nesse laboratório, foi implementado a lógica de um jogo fictício. Aloy é uma caçadora e arqueira, que utiliza a velocidade, esperteza e agilidade para
permanecer viva e proteger sua tribo, em um mundo pós-apocalíptico dominado por criaturas mecanizadas como animais robôs colossais.
Aloy possui um dispositivo chamado Foco, que lhe permite escanear objetos e criaturas para obter informações como quanto dano já levou, a fraqueza das máquinas
e quanto de dano os monstros levam ao serem acertados. Os componentes destas criaturas são complexos e delicados. Tais componentes, ou partes, costumam receber 
mais dano quando acertados em locais específicos (pontos críticos), além de possuírem vulnerabilidades a determinados elementos.
Informações mais específicas serão detalhadas junto com o exemplo de entrada e saída abaixo.
'''

class Aloy():
    def __init__(self, vida):
        self.vida = vida
    def atualiza_vida(self,dano):
        self.vida -= dano


class Maquina:
    def __init__(self, vida, dano_ataque, quantidade_partes):
        self.vida = vida
        self.dano_ataque = dano_ataque
        self.quantidade_partes = quantidade_partes
        self.partes = dict().copy()
    def atualiza_vida(self,dano):
        self.vida -= dano
  

class Parte:
    def __init__(self, parte, fraqueza, dano_maximo, cx, cy):
        self.parte = parte
        self.fraqueza = fraqueza
        self.dano_maximo = dano_maximo
        self.cx = cx
        self.cy = cy


def main():
    vida = int(input())
    primeira_vida = vida
    vida_inicial = vida
    aloy = Aloy(vida)
    dados_flechas = input().split()
    flechas = {}
    dic_flechas_utilizadas = {}
    i = 0
    while i < len(dados_flechas):
       flechas[dados_flechas[i]] = int(dados_flechas[i + 1])
       dic_flechas_utilizadas[dados_flechas[i]] = 0
       i += 2
    numero_maquinas = int(input())    
    maquinas_enfrentadas = 0
    maquinas_enfrentadas_agora = 0
    dic_criticos = {}
    indice_combate = -1
    dic_combates = {}
    flechas_copia = flechas.copy()
    lista_combates = []
    while maquinas_enfrentadas < numero_maquinas:
        if verifica_vida_aloy(aloy) == False:
            break
        if verifica_quantidade_flechas == False:
            break
        indice_combate += 1
        input_maquinas_enfrentadas = int(input())
        maquinas_enfrentadas += input_maquinas_enfrentadas
        maquinas_enfrentadas_agora = input_maquinas_enfrentadas
        lista_maquinas = []
        contador_ataque = 0
        lista_maquinas_derrotadas = []
        for num_maquina in range(maquinas_enfrentadas_agora):
            dic_criticos[num_maquina] = {}
            informacoes_maquinas = input().split(' ')
            maquina = Maquina(vida = int(informacoes_maquinas[0]), dano_ataque = int(informacoes_maquinas[1]), quantidade_partes = int(informacoes_maquinas[2]))
            for _ in range(maquina.quantidade_partes):
                parte_maquina = input().split(', ')
                maquina.partes[parte_maquina[0]] = Parte(parte= parte_maquina[0], fraqueza= parte_maquina[1], dano_maximo= int(parte_maquina[2]), cx= int(parte_maquina[3]), cy= int(parte_maquina[4]))
                dic_criticos[num_maquina][int(parte_maquina[3]), int(parte_maquina[4])] = 0
            lista_maquinas.append(maquina)
        while verifica_vida_maquinas(lista_maquinas) == True:
            informacoes_alvo = input().split(', ')
            if flechas_copia[informacoes_alvo[2]] > 0:
                flechas_copia[informacoes_alvo[2]] -= 1
            else:
                saida_sem_flechas(indice_combate, aloy, vida_inicial, lista_maquinas_derrotadas)
                break
            unidade_alvo = int(informacoes_alvo[0])
            dano_causado_aloy = calcula_dano(informacoes_alvo, lista_maquinas[unidade_alvo])
            lista_maquinas[unidade_alvo].atualiza_vida(dano_causado_aloy)
            if lista_maquinas[unidade_alvo].vida <= 0:
                lista_maquinas_derrotadas.append(unidade_alvo)
            dic_flechas_utilizadas[informacoes_alvo[2]] += 1
            contador_ataque += 1
            if contador_ataque == 3:
                dano = calcula_dano_maquina(lista_maquinas)
                if verifica_vida_maquinas(lista_maquinas) == True:
                    aloy.atualiza_vida(dano)
                    contador_ataque = 0
            if (int(informacoes_alvo[3]), int(informacoes_alvo[4])) == (lista_maquinas[unidade_alvo].partes[informacoes_alvo[1]].cx, lista_maquinas[unidade_alvo].partes[informacoes_alvo[1]].cy):
                dic_criticos[unidade_alvo][(int(informacoes_alvo[3]), int(informacoes_alvo[4]))] += 1
            if verifica_vida_maquinas(lista_maquinas) == False:
                dic_combates[f'combate {indice_combate}'] = 'vitória'
                lista_combates.append('vitoria')
                saida_vitoria(indice_combate, aloy, vida_inicial, lista_maquinas_derrotadas, flechas, dic_flechas_utilizadas, dic_criticos)
            elif verifica_quantidade_flechas(flechas_copia) == False:
                dic_combates[f'combate {indice_combate}'] = 'sem flechas'
                lista_combates.append('sem flechas')
                saida_sem_flechas(indice_combate, aloy, vida_inicial, lista_maquinas_derrotadas)
            elif aloy.vida <= 0:
                aloy.vida = max(aloy.vida, 0)
                dic_combates[f'combate {indice_combate}'] = 'derrota'
                lista_combates.append('derrota')
                saida_derrota(indice_combate, aloy, vida_inicial, lista_maquinas_derrotadas)
            if verifica_vida_aloy(aloy) == False:
                break
        for flecha in flechas:
            dic_flechas_utilizadas[flecha] = 0
        flechas_copia = flechas.copy()
        dic_criticos = {}
        if aloy.vida > 0:
            vida_inicial = recupera_vida(aloy, vida_inicial, primeira_vida)
    verifica_vitoria(lista_combates)


def verifica_vida_maquinas(todas_maquinas):
    maquinas = False
    for maquina in todas_maquinas:
        if maquina.vida > 0:
            return True
    return maquinas


def verifica_vida_aloy(aloy):
    vida = False
    if aloy.vida > 0:
        return True
    return vida


def verifica_quantidade_flechas(flechas_copia):
    condicao = False
    for flecha in flechas_copia:
        if flechas_copia[flecha] != 0:
            return True
    return condicao


def calcula_dano_maquina(lista_maquinas):
    dano_maquinas = 0
    for maquina in lista_maquinas:
        if maquina.vida > 0:
            dano_maquinas += maquina.dano_ataque
    return dano_maquinas


def verifica_vitoria(lista_combates):
    resultado = 0
    numero_minimo = 0
    while resultado < len(lista_combates):
        if lista_combates[resultado] == 'derrota' or lista_combates[resultado] == 'sem flechas':
            numero_minimo += 1
        resultado += 1
    if numero_minimo == 0:
        print('Aloy provou seu valor e voltou para sua tribo.')


def calcula_dano(informacoes_alvo, maquina):
    ''' Calcula o dano '''
    dano = maquina.partes[informacoes_alvo[1]].dano_maximo - (abs(int((maquina.partes[informacoes_alvo[1]].cx) - int(informacoes_alvo[3]))) + abs(int(maquina.partes[informacoes_alvo[1]].cy) - int(informacoes_alvo[4])))
    if maquina.partes[informacoes_alvo[1]].fraqueza == 'todas':
        dano = max(dano, 0)
        return dano
    elif informacoes_alvo[2] != maquina.partes[informacoes_alvo[1]].fraqueza or maquina.partes[informacoes_alvo[1]].fraqueza == 'nenhuma':
        dano = max(dano, 0)
        dano = dano // 2
        return dano
    else:
        return max(dano, 0)


def recupera_vida(aloy, vida_inicial, primeira_vida):
    aloy.vida += vida_inicial // 2
    if aloy.vida > primeira_vida:
        aloy.vida = primeira_vida
    return aloy.vida


def checa_criticos(dic_criticos):
    soma_criticos = 0
    for maquina in dic_criticos: 
        for critico in dic_criticos[maquina]:
            soma_criticos += dic_criticos[maquina][critico]
    if soma_criticos == 0:
        return 'sem criticos'
    else:
        return None


def checa_criticos_maquinas(dic_criticos, maquina):
    condicao = False
    for critico in dic_criticos[maquina]:
        if dic_criticos[maquina][critico] != 0:
            return True
    return condicao

def saida_vitoria(indice_combate, aloy, vida_inicial, maquinas_derrotadas, flechas, dic_flechas_utilizadas, dic_criticos):
    print(f'Combate {indice_combate}, vida = {vida_inicial}')
    for maquina in maquinas_derrotadas:
        print(f'Máquina {maquina} derrotada')
    print(f'Vida após o combate = {aloy.vida}')
    print('Flechas utilizadas:')
    for tipo_flecha in dic_flechas_utilizadas:
        if dic_flechas_utilizadas[tipo_flecha] != 0:
            print(f'- {tipo_flecha}: {dic_flechas_utilizadas[tipo_flecha]}/{flechas[tipo_flecha]}')
    if checa_criticos(dic_criticos) == None:
        print('Críticos acertados:')
    for maquina in dic_criticos:
        if checa_criticos_maquinas(dic_criticos, maquina) == True:  
            print(f'Máquina {maquina}:')
            for critico in dic_criticos[maquina]:
                if dic_criticos[maquina][critico] > 0:
                    print(f'- {critico}: {dic_criticos[maquina][critico]}x')


def saida_derrota(indice_combate, aloy, vida_inicial, maquinas_derrotadas):
    print(f'Combate {indice_combate}, vida = {vida_inicial}')
    for maquina in maquinas_derrotadas:
        print(f'Máquina {maquina} derrotada')
    print(f'Vida após o combate = {aloy.vida}')
    print('Aloy foi derrotada em combate e não retornará a tribo.')


def saida_sem_flechas(indice_combate, aloy, vida_inicial, maquinas_derrotadas):
    print(f'Combate {indice_combate}, vida = {vida_inicial}')
    for maquina in maquinas_derrotadas:
        print(f'Máquina {maquina} derrotada')
    print(f'Vida após o combate = {aloy.vida}')
    print('Aloy ficou sem flechas e recomeçará sua missão mais preparada.')


if __name__ == '__main__':
    main()


'''
Aloy deverá derrotar uma quantia N demáquinas, sendo que pode enfrentar até U (1 ≤ U ≤ N) 
máquinas ao mesmo tempo. Comouma caçadora experiente e veloz, ela consegue disparar 3 flechas 
seguidas antes dereceber dano de todas as U máquinas inimigas. Essas flechas podem acertar pontos
diferentes em partes diferentes e ter máquinas diferentes como alvo. Em relação às máquinas, cada uma
de suas partes possui um valor de dano máximo (M) em relação aos pontos totais de vida da máquina (V).
O cálculo de dano (D) funciona da seguinte maneira:

1. Caso a flecha seja do mesmo tipo da fraqueza e ela acerte um ponto qualquer(fx,fy),
o dano causado será igual à diferença entre o dano máximo e a Distância de
Manhattan entre o ponto de crítico (cx,cy) e o ponto acertado, ou seja:

D = M − (|(cx − fx)| + |(cy − fy)|)

2. Caso a flecha acerte um ponto qualquer e ela não for do mesmo tipo da fraqueza, o
dano será igual a D (como definido acima) dividido por 2. Você deve utilizar a divisão
inteira para não ocorrerem problemas de precisão.

O Foco faz com que Aloy esteja ciente das fraquezas das peças (podendo ser todas ou
nenhuma), sendo assim, ela sempre usará os tipos de flechas compatíveis, caso estejam
disponíveis. Fazer flechas diferentes gasta muitos recursos, então após o final do
combate ela vai até as coordenadas de acerto de cada flecha e as recolhe, a fim de
manter seu estoque. Além disso, ao final de cada combate ela toma um remédio, que
recupera seus pontos de vida em até 50% dos pontos de vida máximos, isto é, os
pontos de vida de Aloy após se curar serão acrescidos de floor(0,5 × vida máxima), desde
que não ultrapassem os pontos de vida máximos.

Exemplo

Entrada
500
confusão 20 fogo 10 gelo 15 normal 50 perfurante 20 veneno 15
1
1
90 5 2
corpo, nenhuma, 90, 0, 0
olho, todas, 180, 0, 10
0, olho, perfurante, 0, 10

Saída
Combate 0, vida = 500
Máquina 0 derrotada
Vida após o combate = 500
Flechas utilizadas:
- perfurante: 1/20
Críticos acertados:
Máquina 0:
- (0, 10): 1x
Aloy provou seu valor e voltou para sua tribo.
'''
