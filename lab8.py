'''
Nesse laboratório, foi criado um sistema para calcular a premiação de filmes de uma cerimônia fictícia.
Os filmes indicados concorrem a 7 categorias no total, 5 simples e 2 especiais.
O vencedor de cada categoria simples é determinado por uma pontuação obtida a partir de notas dadas pelos avaliadores, tendo a maior média aritmética.
O vencedor de cada categoria especial é definido de maneira diferente:
Categoria Prêmio Pior Filme do Ano: o filme que ganhar mais categorias simplees vence, caso houver empate, o vencedor deve ser o filme que obteve a maior quantidade de pontos no total.
Categoria Não Merecia Estar Aqui: vence aqueles um ou mais filmes que não foram avaliados, caso todos os filmes tenham sido escolhidos, o código informa que ninguém venceu.
'''
def calcula_media_notas(categoria_filme_nota):
    categoria_filme_media = {}
    for categoria in categoria_filme_nota:
        categoria_filme_media[categoria] = categoria_filme_nota[categoria].copy()
        for filme in categoria_filme_nota[categoria]:
            categoria_filme_media[categoria][filme] = categoria_filme_nota[categoria][filme].copy()    
    for categoria in categoria_filme_media:
            for filme in categoria_filme_media[categoria]:
                soma_pontos = sum(categoria_filme_media[categoria][filme])
                media = soma_pontos / len(categoria_filme_media[categoria][filme])
                categoria_filme_media[categoria][filme] = media

    return categoria_filme_media


def define_vencedores_categoria_simples(medias_notas, categoria_filme_nota, categorias_simples):
    categoria_filme_vencedor = {}
    criterio_desempate = 0
    for categoria in categorias_simples:
        if medias_notas[categoria] != {}:
            valores = list(medias_notas[categoria].values())
            maior_nota = max(valores)
            criterio_empate_1 = valores.count(maior_nota)
            lista_chaves_valores = list(medias_notas[categoria].items())
            if criterio_empate_1 == 1:
                for i in lista_chaves_valores:
                    if i[1] == maior_nota:
                        filme = i[0]
                        categoria_filme_vencedor[categoria] = filme
            elif criterio_empate_1 > 1:
                    for filme in categoria_filme_nota[categoria]:
                        lista_filmes = list(medias_notas[categoria].keys())
                        criterio_empate_2 = lista_filmes.count(filme)
                        if len(categoria_filme_nota[categoria][filme]) + criterio_empate_2 > criterio_desempate:
                            criterio_desempate = len(categoria_filme_nota[categoria][filme])
                            categoria_filme_vencedor[categoria] = filme
            
    return categoria_filme_vencedor


def define_vencedores_categorias_especiais(vencedores_categorias_simples,lista_nomes, media_notas, categoria_filme_nota):
    for categoria in vencedores_categorias_simples:
        filmes_vencedores = list(vencedores_categorias_simples.values())
        lista_repeticoes_numeros = []
        dicionarios_repeticoes_nomes = {}
        dicionarios_soma_media_filme = {}
        lista_somas_medias = []
        valor_minimo = 0
        filme_anterior = 0
        for filme in filmes_vencedores:
            if filme != filme_anterior:
                filme_anterior = filme
                numero_repeticoes = filmes_vencedores.count(filme)
                lista_repeticoes_numeros.append(numero_repeticoes)
                dicionarios_repeticoes_nomes[numero_repeticoes] = filme
                if lista_repeticoes_numeros.count(max(lista_repeticoes_numeros)) == 1 and max(lista_repeticoes_numeros) > valor_minimo:
                    valor_minimo = max(lista_repeticoes_numeros)
                    vencedor_PPFA = dicionarios_repeticoes_nomes[max(lista_repeticoes_numeros)]
                elif lista_repeticoes_numeros.count(max(lista_repeticoes_numeros)) > 1:
                    for filme in filmes_vencedores:
                        soma_media = 0
                        for categoria in media_notas:
                            if filme in media_notas[categoria]:    
                                soma_media += media_notas[categoria][filme]
                        lista_somas_medias.append(soma_media)
                        dicionarios_soma_media_filme[soma_media] = filme
                    vencedor_PPFA = dicionarios_soma_media_filme[max(lista_somas_medias)]
    dicionario_vencedores_NDEA = {}
    lista_vencedores = []
    for nome in lista_nomes:
        n = 0
        for categoria in categoria_filme_nota:
            if nome not in categoria_filme_nota[categoria]:
                n += 1
            dicionario_vencedores_NDEA[nome] = n
    lista_nomes_dicionario = list(dicionario_vencedores_NDEA.items())
    for i in range(len(lista_nomes_dicionario)):
        if lista_nomes_dicionario[i][1] == 5:
            lista_vencedores.append(lista_nomes_dicionario[i][0])
    vencedores_NDEA = lista_vencedores
        
    return  vencedor_PPFA, vencedores_NDEA


def saida(categoria_filme_vencedor, vencedor_PPFA, vencedores_NDEA):
    print('#### abacaxi de ouro ####''\n')
    print('categorias simples')
    for categoria in categoria_filme_vencedor:
        print('categoria:',categoria+'\n'+'-', categoria_filme_vencedor[categoria])
    print('\n''categorias especiais')
    print('prêmio pior filme do ano')
    print('-', vencedor_PPFA)
    print('prêmio não merecia estar aqui')
    if vencedores_NDEA == []:
        print('- sem ganhadores')
    else:
        print('-', ', '.join(vencedores_NDEA))

def main():
    categorias_simples = {'filme que causou mais bocejos': 0, 'filme que foi mais pausado': 0, 'filme que mais revirou olhos': 0, 'filme que não gerou discussão nas redes sociais': 0, 'enredo mais sem noção': 0}
    categoria_filme_nota = categorias_simples.copy()
    for categoria in categorias_simples:
        categoria_filme_nota[categoria] = {}
    lista_nomes = []
    f = int(input())
    for _ in range(f):
        nome_filme = input()
        lista_nomes.append(nome_filme)

    q = int(input())
    for _ in range(q):
        dados_filme = input().split(', ')
        if dados_filme[2] not in categoria_filme_nota[dados_filme[1]]:
            categoria_filme_nota[dados_filme[1]][dados_filme[2]] = []
        dados_filme[3] = int(dados_filme[3])
        categoria_filme_nota[dados_filme[1]][dados_filme[2]].append(dados_filme[3])
    
    medias_notas = calcula_media_notas(categoria_filme_nota)
    vencedores_categoria_simples = define_vencedores_categoria_simples(medias_notas, categoria_filme_nota, categorias_simples)
    vencedor_PPFA, vencedores_NDEA = define_vencedores_categorias_especiais(vencedores_categoria_simples, lista_nomes, medias_notas, categoria_filme_nota )
    saida(vencedores_categoria_simples, vencedor_PPFA, vencedores_NDEA)


if __name__ == '__main__':
    main()

'''
Exemplo 

Entrada
4
a força da amizade
elas por elas
ninguém é de ninguém
o portal secreto
20
avaliador 2, filme que causou mais bocejos, ninguém é de ninguém,
2
avaliador 3, enredo mais sem noção, o portal secreto, 9
avaliador 3, filme que não gerou discussão nas redes sociais,
elas por elas, 6
avaliador 2, filme que causou mais bocejos, o portal secreto, 6
avaliador 3, filme que mais revirou olhos, o portal secreto, 4
avaliador 2, filme que não gerou discussão nas redes sociais,
ninguém é de ninguém, 6
avaliador 1, filme que causou mais bocejos, ninguém é de ninguém,
7
avaliador 1, filme que foi mais pausado, ninguém é de ninguém, 3
avaliador 2, enredo mais sem noção, o portal secreto, 8
avaliador 3, filme que causou mais bocejos, a força da amizade, 3
avaliador 1, filme que não gerou discussão nas redes sociais,
elas por elas, 9
avaliador 3, filme que foi mais pausado, a força da amizade, 8
avaliador 1, filme que mais revirou olhos, o portal secreto, 8
avaliador 3, enredo mais sem noção, elas por elas, 6
avaliador 2, filme que mais revirou olhos, a força da amizade, 3
avaliador 3, filme que causou mais bocejos, o portal secreto, 8
avaliador 1, filme que foi mais pausado, a força da amizade, 5
avaliador 1, enredo mais sem noção, o portal secreto, 3
avaliador 2, filme que mais revirou olhos, ninguém é de ninguém,
4
avaliador 3, enredo mais sem noção, a força da amizade, 5

Saída
#### abacaxi de ouro ####
categorias simples
categoria: filme que causou mais bocejos
- o portal secreto
categoria: filme que foi mais pausado
- a força da amizade

categoria: filme que mais revirou olhos
- o portal secreto
categoria: filme que não gerou discussão nas redes sociais
- elas por elas
categoria: enredo mais sem noção
- o portal secreto
categorias especiais
prêmio pior filme do ano
- o portal secreto
prêmio não merecia estar aqui
- sem ganhadores
'''
