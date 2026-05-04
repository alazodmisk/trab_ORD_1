import sys

class ChavePrincipal:
    def __init__(self, indice: int, offset: int):
        self.indice = indice
        self.offset = offset

class ChaveSecundaria:
    def __init__(self, nome: str, indice: int):
        self.nome = nome 
        self.indice = indice #Prox caso de *nome*
        

class Indices:
    def __init__(self, indice: int, proxGenero: int, proxPublicadora: int):
        self.indice = indice
        self.proxGenero = proxGenero
        self.proxPublicadora = proxPublicadora


#FUNÇÕES AUXILIARES
def busca_binaria_chPrincipal(argumento: int, lista: list[ChavePrincipal]) -> int:
    inicio = 0
    final = len(lista) - 1

    while inicio <= final:
        media = (inicio+final)//2
        if lista[media].indice == argumento:
            return media
        elif lista[media].indice < argumento:
            inicio = media + 1
        else:
            final = media - 1
    return -1

def busca_binaria_chSecundaria(argumento: str, lista: list[ChaveSecundaria]) -> int:
    inicio = 0
    final = len(lista) - 1

    while inicio <= final:
        media = (inicio+final)//2
        if lista[media].nome == argumento:
            return lista[media].indice
        elif lista[media].nome < argumento:
            inicio = media + 1
        else:
            final = media - 1
    return -1

def organiza_lista_chPrincipal(lista: list[ChavePrincipal]) -> None:
    for i in range(len(lista)-1):
        if lista[i].indice > lista[i+1].indice:
            aux = lista[i+1]
            lista[i+1] = lista[i]
            lista[i] = aux
        else:
            break
        
def organiza_lista_chSecundaria(lista: list[ChaveSecundaria]) -> None:
    for i in range(len(lista)-1):
        if lista[i].nome > lista[i+1].nome:
            aux = lista[i+1]
            lista[i+1] = lista[i]
            lista[i] = aux
        else:
            break
# 2, 0, 348, [[484, -1, -1]], [[Nintendo, 0]]
def organiza_proxs(qualChave: int, posicaoLista: int, idNovo: int, invertida: list[Indices], lista: list[ChaveSecundaria]) -> int:
    final = len(invertida)
    posicao = lista[posicao].indice

    if invertida[posicao].indice > idNovo:
        lista[posicao].indice = final

    elif qualChave == 1:#ANALISE DE GENERO  
        while invertida[posicao].proxGenero != -1 and invertida[invertida[posicao].proxGenero].indice < idNovo:
            posicao = invertida[posicao].proxGenero
        
        aux = invertida[posicao].proxGenero
        invertida[posicao].proxGenero = final
        posicao = aux

    else:               #ANALISE DE PUBLICADORA
        while invertida[posicao].proxPublicadora != -1 and invertida[invertida[posicao].proxPublicadora].indice < idNovo:
            posicao = invertida[posicao].proxPublicadora
        
        aux = invertida[posicao].proxPublicadora
        invertida[posicao].proxPublicadora = final
        posicao = aux

    return posicao




def construir_indices():
    primarioLista: list[ChavePrincipal] = []
    generoLista: list[ChaveSecundaria] = []
    publicadoraLista: list[ChaveSecundaria] = []
    listaInvertida: list[Indices] = []
    offset: int = 0

    with open('games.dat', 'rb') as games:
        buffer = games.read(2)

        while buffer != b'':

            retorno = []
            for i in generoLista:
                retorno += [[i.nome, i.indice]]
            print(retorno)
            print()

            retorno = []
            for i in publicadoraLista:
                retorno += [[i.nome, i.indice]]
            print(retorno)
            print()

            retorno = []
            for i in listaInvertida:
                retorno += [[i.indice, i.proxGenero, i.proxPublicadora]]
            print(retorno)
            print()

            tam = int.from_bytes(buffer, "little")
            buffer = games.read(tam).decode()

            registro:list[str] = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]

            indice = int(registro[0])

            primarioLista = [ChavePrincipal(indice, offset)] + primarioLista
            organiza_lista_chPrincipal(primarioLista)
            offset += tam + 2

            finalLista = len(listaInvertida)

            print(f"{registro[0]}: {registro[3]} from {registro[4]}")

            posicaoGen = busca_binaria_chSecundaria(registro[3], generoLista)
            if posicaoGen == -1:
                generoLista = [ChaveSecundaria(registro[3], finalLista)] + generoLista
                organiza_lista_chSecundaria(generoLista)
            else:
                posicaoGen = organiza_proxs(1, posicaoGen, indice, listaInvertida, generoLista)
            

            posicaoPubl = busca_binaria_chSecundaria(registro[4], publicadoraLista)
            if posicaoPubl == -1:
                publicadoraLista = [ChaveSecundaria(registro[4], finalLista)] + publicadoraLista
                organiza_lista_chSecundaria(publicadoraLista)
            else:
                posicaoPubl = organiza_proxs(2, posicaoPubl, indice, listaInvertida, publicadoraLista)
            
            listaInvertida += [Indices(indice, posicaoGen, posicaoPubl)]

            buffer = games.read(2)


    with open("primario.ind", "w+") as primario:
        for i in primarioLista:
            linha = str(i.indice) + " " + str(i.offset)
            primario.write(linha + "\n") 

    with open("publicadora.ind", "w+") as publicadora:
        for i in publicadoraLista:
            linha = str(i.indice) + " " + i.nome
            publicadora.write(linha + "\n") 
            
    with open("genero.ind", "w+") as genero:
        for i in generoLista:
            linha = str(i.indice) + " " + i.nome
            genero.write(linha + "\n") 

    with open("listaInvertida.lst", "w+") as listaTotal:
        for i in listaInvertida:
            linha = str(i.indice) + " " + str(i.proxGenero) + " " + str(i.proxPublicadora)
            listaTotal.write(linha + "\n") 

    

##FUNÇÕES AUXILIARES DA EXECUÇÃO DAS OPERAÇÕES
def busca_indice_primario():
    print("Iniciando a busca...")
    ''' abre o primario.ind
        trasnforma os elem do primario.ind em objetos e sobe no primarioLista
        iteração
            procura indice primario por meio de busca binária
            
        se achou
            verifica o byteoffsett
        se não
            fala que nao achou
            
        abre o games.dat
            faz o seek no byte offset
            imprime o registro
    '''
    
def busca_indice_genero():
    print("Iniciando a busca pelo indice secundário: Gênero...")

def busca_indice_publicadora():
    print("Iniciando a busca pelo indice secundário: publicadora...")

def insercao(argumento: str):
    print("Iniciando a inserção...")
    ''' 

    Salva o offset como o tamanho de games.dat
    Abre primario.ind, procura o Genero do meliante
    caso ja exista -> faça manutençao dos id dos generos
    caso nao -> add em genero.ind
    msm coisa com publicadora
    
    escreve no offset de games.dat, ou seja no final
    com .sizeof do inserido'''
    # tamanho = len(argumento).to_bytes()
    # registro = argumento.split('|')
    # offset = 0 #N SEI COMO MECHER COM ISSO

    # with open("game.dat", 'r') as game:
    # with open("primario.ind", 'r') as p:
    #     buffer = p.read().decode()
    #     dados = buffer.split('\n')
    #     dados.pop()
    #     for i in dados:
    #         i = i.split(' ', 1)
        
    #     inicio = 0
    #     final = len(dados) - 1
    #     posicao = -1

    #     if registro[0] != dados[inicio] and registro[0] != dados[final]:
    #         if registro[0] < dados[inicio]:
    #             dados = Identificador(registro[0], offset) + dados
    #         elif registro[0] > dados[final]:
    #             dados = dados + Identificador(registro[0], offset)
    #         else: 
    #             while inicio < final and posicao == -1:
    #                 media = (inicio + final)//2
    #                 if dados[media] == registro[0]:
    #                     break
    #                 if registro[0] > dados[media]:
    #                     inicio = media + 1
    #                     if registro[0] < dados[media+1]:
    #                         posicao = media
                        
    #                 if registro[0] < dados[media]:
    #                     final = media - 1
    #                     if registro[0] > dados[media-1]:
    #                         posicao = media - 1
    #             if posicao == -1:
    #                 print()
    #             else:
    #                 dados = dados[:posicao] + Identificador(registro[0], EITAPORRA) + dados[posicao:]   

def remocao():
    print("Iniciando a remoção...")


##FUNÇÃO PRINCIPAL DA EXECUÇÃO DAS OPERAÇÕES
def executar_operacoes(nome_arquivo):
    print(f"Executando operações do arquivo: {nome_arquivo}")
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()

                if not linha:
                    continue  # pula linha vazia
                
                partes = linha.split(" ", 1)
                operacao = partes[0]
                argumento = partes[1]

                if operacao == 'bp':
                    busca_indice_primario()
                elif operacao == 'bs1':
                    busca_indice_genero()
                elif operacao == 'bs2':
                    busca_indice_publicadora()
                elif operacao == 'i':
                    insercao(argumento)
                elif operacao == "r":
                    remocao()
                else:
                    print("Comando não identificado. Por favor, verifique se o arquivo de operações.")    

    except FileNotFoundError:
        print("Erro: arquivo de operações não encontrado.")

def compactar_arquivo():
    print("Iniciando a compactação do arquivo...")

def main():
    if len(sys.argv) < 2:
        print("Erro: Use as flags -b, -e ou -c.")
        return

    flag = sys.argv[1]

    if flag == '-b':
        construir_indices()

    elif flag == '-e':
        if len(sys.argv) < 3:
            print("Erro: Para usar -e, você deve informar o arquivo de operações.")
        else:
            arquivo_ops = sys.argv[2]
            executar_operacoes(arquivo_ops)

    elif flag == '-c':
        compactar_arquivo()
        
    else:
        print(f"Flag '{flag}' não reconhecida.")

if __name__ == "__main__":
    main()                                                         
