import io
import os
import sys
import struct


fmtPrimario = '<HI'
fmtSecundario = '30sH'
fmtInvertido = '<3h'


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


def busca_binaria_chPrincipal(argumento: int, lista: list[ChavePrincipal]) -> int:
    '''Funções busca_binaria_chPrincipal(argumento, lista) e busca_binaria_chSecundaria(argumento,
    lista) utilizadas para encontrar a posição de um *argumento* em *lista*.
    Retorna -1 caso não esteja presente'''
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
            return media
        elif lista[media].nome < argumento:
            inicio = media + 1
        else:
            final = media - 1
    return -1



def organiza_lista_chPrincipal(lista: list[ChavePrincipal]) -> None:
    '''Funções organiza_lista_chPrincipal(lista) e organiza_lista_chSecundaria(lista) utilizadas para
    organizar listas quando há inserção de uma nova chave em *lista*.
    Método de Insertion Sort, analisando a posição ideal de um novo ID inserido no começo.'''
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

def organiza_proxs(idNovo: int, qualChave: int, posicaoLista: int, invertida: list[Indices], lista: list[ChaveSecundaria]) -> int:
    '''Existem dois casos de Organizacao:
    - Por Genero =       organiza_prox(*idNovo*, 1, *posicaoLista*, invertidaLista, generoLista)
    - Por Publicadora =  organiza_prox(*idNovo*, 2, *posicaoLista*, invertidaLista, publicadoraLista)

    dessa forma temos *qualChave* para diferenciar entre organizacao por Genero (1) e por Publicadora
    (2), para podermos atualizar os .prox de *invertida* e, caso o primeiro caso de uma chaveSecundaria
    seja alterado, atualizar a *lista*.
    Atualizações de acordo com o *idNovo* comecando por *posicaoLista* (primeiro caso de chaveSecundaria
    encontrado.)'''

    final = len(invertida)
    posicao = lista[posicaoLista].indice

    if invertida[posicao].indice > idNovo:
        lista[posicaoLista].indice = final

    elif qualChave == 1:    #ANALISE DE GENERO
        while invertida[posicao].proxGenero != -1 and invertida[invertida[posicao].proxGenero].indice < idNovo:
            posicao = invertida[posicao].proxGenero
        
        aux = invertida[posicao].proxGenero
        invertida[posicao].proxGenero = final
        posicao = aux

    else:                   #ANALISE DE PUBLICADORA
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
            tam = int.from_bytes(buffer, "little")
            buffer = games.read(tam).decode()

            registro:list[str] = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]

            if registro[0][0] == '*':
                buffer = games.read(2)
                offset += tam + 2
                continue

            indice = int(registro[0])

            primarioLista = [ChavePrincipal(indice, offset)] + primarioLista
            organiza_lista_chPrincipal(primarioLista)
            offset += tam + 2

            finalLista = len(listaInvertida)

            
            posicaoGen = busca_binaria_chSecundaria(registro[3], generoLista)
            if posicaoGen == -1:
                generoLista = [ChaveSecundaria(registro[3], finalLista)] + generoLista
                organiza_lista_chSecundaria(generoLista)
            else:
                posicaoGen = organiza_proxs(indice, 1, posicaoGen, listaInvertida, generoLista)
            
            
            posicaoPubl = busca_binaria_chSecundaria(registro[4], publicadoraLista)
            if posicaoPubl == -1:
                publicadoraLista = [ChaveSecundaria(registro[4], finalLista)] + publicadoraLista
                organiza_lista_chSecundaria(publicadoraLista)
            else:
                posicaoPubl = organiza_proxs(indice, 2, posicaoPubl, listaInvertida, publicadoraLista)
            
            listaInvertida += [Indices(indice, posicaoGen, posicaoPubl)]
            buffer = games.read(2)


    with open("primario.ind", "wb") as primario:
        for i in primarioLista:
            linha = struct.pack(fmtPrimario, i.indice, i.offset)
            primario.write(linha) 

    with open("publicadora.ind", "wb") as publicadora:
        for i in publicadoraLista:
            linha = struct.pack(fmtSecundario, i.nome.encode(), i.indice)
            publicadora.write(linha) 
            
    with open("genero.ind", "wb") as genero:
        for i in generoLista:
            linha = struct.pack(fmtSecundario, i.nome.encode(), i.indice)
            genero.write(linha) 

    with open("listaInvertida.lst", "wb") as listaTotal:
        for i in listaInvertida:
            linha = struct.pack(fmtInvertido, i.indice, i.proxGenero, i.proxPublicadora)
            listaTotal.write(linha)  


def carrega_indices(arq: io.BufferedReader, codigo: int):
    lista: list[ChavePrincipal| ChaveSecundaria |Indices] = []

    if codigo == 1:
        fmt = fmtPrimario
        tam = struct.calcsize(fmtPrimario)
    elif codigo == 2:
        fmt = fmtSecundario
        tam = struct.calcsize(fmtSecundario)
    else:
        fmt = fmtInvertido
        tam = struct.calcsize(fmtInvertido)
        
    linha = arq.read(tam)
    while len(linha) == tam:
        buffer = struct.unpack(fmt, linha)

        if codigo == 1:
            lista.append(ChavePrincipal(buffer[0], buffer[1]))
        elif codigo == 2:
            nome = buffer[0].decode().strip('\x00')
            lista.append(ChaveSecundaria(nome, buffer[1]))
        else:
            lista.append(Indices(buffer[0], buffer[1], buffer[2]))

        linha = arq.read(tam)

    return lista

def busca_indice_primario(listas: list[ChavePrincipal], argumento: int, games: io.BufferedRandom):
    '''Função carregar_indice_primario() utilizada para ler o arquivo "primario.ind"
    e transformar cada linha em um objeto do tipo ChavePrincipal, armazenando-os
    em uma lista.

    Cada linha do arquivo deve estar no formato:
        <indice> <offset>

    Onde:
        - indice: identificador único do registro
        - offset: posição em bytes do registro no arquivo "games.dat"

    A função ignora linhas vazias e converte os valores para inteiro antes de
    criar os objetos.

    Retorna:
    - lista contendo objetos ChavePrincipal com indice e offset correspondentes'''
    primarioLista: list[ChavePrincipal] = listas[0]

    print(f'Buscando registro de ID "{argumento}"')

    pos = busca_binaria_chPrincipal(argumento, primarioLista)
    if pos != -1:
        offset = primarioLista[pos].offset

        games.seek(offset)
        tam = int.from_bytes(games.read(2), "little")
        registro = games.read(tam).decode()
        print("- " + registro)
    else:
        print("- Registro não encontrado! <índice inválido>")

def busca_indice_secundario(listas:list[list[ChavePrincipal]|list[ChaveSecundaria]|list[Indices]], codigo: int, argumento: str, games: io.BufferedRandom):
    primarioLista: list[ChavePrincipal] = listas[0]
    secundarioLista: list[ChaveSecundaria] = listas[codigo]
    listaInvertida: list[Indices] = listas[3]

    print(f'Buscando registros de "{argumento}"')

    pos = busca_binaria_chSecundaria(argumento, secundarioLista)
    if pos == -1:
        if codigo == 1:
            print("- Gênero não encontrado!")
        else:
            print("- Publicadora não encontrada!")
        return

    atual = secundarioLista[pos].indice
    while atual != -1:
        no = listaInvertida[atual]
        posPrim = busca_binaria_chPrincipal(no.indice, primarioLista)

        offset = primarioLista[posPrim].offset
        games.seek(offset)
        tam = int.from_bytes(games.read(2), "little")
        registro = games.read(tam).decode()
        print("- " + registro)

        if codigo == 1:
            atual = no.proxGenero
        else:
            atual = no.proxPublicadora


def insercao(listas: list[list[ChavePrincipal]|list[ChaveSecundaria]|list[Indices]], argumento: str, games: io.BufferedRandom) -> list:
    registro = argumento.split('|')
    indice = int(registro[0])

    print(f'Inserção do registro de chave "{indice}"')

    pos = busca_binaria_chPrincipal(indice, listas[0])

    if pos == -1:
        games.seek(0, 2)
        finalGames = games.tell()

        listas[0] = [ChavePrincipal(indice, finalGames)] + listas[0]
        organiza_lista_chPrincipal(listas[0])

        posGen = busca_binaria_chSecundaria(registro[3], listas[1])
        if posGen == -1:
            listas[1] = [ChaveSecundaria(registro[3], len(listas[3]))] + listas[1]
            organiza_lista_chSecundaria(listas[1])
        else:
            posGen = organiza_proxs(indice, 1, posGen, listas[3], listas[1])
        

        posPubl = busca_binaria_chSecundaria(registro[4], listas[2])
        if posPubl == -1:
            listas[2] = [ChaveSecundaria(registro[4], len(listas[3]))] + listas[2]
            organiza_lista_chSecundaria(listas[2])
        else:
            posPubl = organiza_proxs(indice, 2, posPubl, listas[3], listas[2])

        listas[3].append(Indices(indice, posGen, posPubl))

        games.write(len(argumento).to_bytes(2, 'little'))
        games.write(argumento.encode())

    else:
        print("- Registro descartado (IDs duplicados não são aceitos).")

    return listas


def remocao(listas: list[list[ChavePrincipal]|list[ChaveSecundaria]|list[Indices]], argumento: int, games: io.BufferedRandom) -> list:
    print(f'Remoção do registro de chave "{argumento}"')
    pos = busca_binaria_chPrincipal(argumento, listas[0])

    if pos != -1:
        offset = listas[0][pos].offset
        listas[0] = listas[0][:pos] + listas[0][pos+1:] # Remocao chPrincipal

        games.seek(offset)
        tamanho = int.from_bytes(games.read(2),'little')
        registro = games.read(tamanho).decode().split('|')

        genero = registro[3]
        publicadora = registro[4]
        
        posSec = busca_binaria_chSecundaria(genero, listas[1])
        posInv = listas[1][posSec].indice
        if listas[3][posInv].proxGenero == -1:
            listas[1] = listas[1][:posSec] + listas[1][posSec + 1:] # Remocao de 1 genero, se só tinha um caso

        elif listas[3][posInv].indice == argumento:
            listas[1][posSec].indice = listas[3][posInv].proxGenero # Alteracao do primeiro caso, se comece com o removido

        else:
            while listas[3][listas[3][posInv].proxGenero].indice != argumento: # Anda até o proximo ser o jogo a ser removido
                posInv = listas[3][posInv].proxGenero
            listas[3][posInv].proxGenero = listas[3][listas[3][posInv].proxGenero].proxGenero
        

        posSec = busca_binaria_chSecundaria(publicadora, listas[2])
        posInv = listas[2][posSec].indice
        if listas[3][posInv].proxPublicadora == -1:
            listas[2] = listas[2][:posSec] + listas[2][posSec + 1:] 

        elif listas[3][posInv].indice == argumento:
            listas[2][posSec].indice = listas[3][posInv].proxPublicadora

        else:
            while listas[3][listas[3][posInv].proxPublicadora].indice != argumento: 
                posInv = listas[3][posInv].proxPublicadora
            listas[3][posInv].proxPublicadora = listas[3][listas[3][posInv].proxPublicadora].proxPublicadora



        #JHONATAN ME AJUDA
        '''for i in range(len(listas[3])):
            if listas[3][i].indice == argumento:
                pos = i
                break

        listas[3] = listas[3][:pos] + listas[3][pos+1:] # Remocao chInvertida

        for i in listas[1]:
            if i.indice > pos:
                i.indice -= 1

        for i in listas[2]:
            if i.indice > pos:
                i.indice -= 1

        for i in listas[3]:
            if i.proxGenero > pos:
                i.proxGenero -= 1
            if i.proxPublicadora > pos:
                i.proxPublicadora -= 1'''


        games.seek(offset + 2)
        games.write(b'*')
        print(f'- "{registro[1]}" removido.')
    else:
        print("- Registro não encontrado!")

    return listas


def compactar_arquivo():
    '''primarioLista: list[ChavePrincipal] = []
    offset = 0'''
    registro:list[str] = []
    validos:list = []
    

    with open('games.dat', 'rb') as gamesDat:
        buffer = gamesDat.read(2)
        while buffer != b'':
            tamanho = int.from_bytes(buffer, 'little')            
            regi1 = gamesDat.read(tamanho)
            regi2 = regi1.decode()
            registro = regi2.split("|")
            id_str = registro[0]
            if not id_str.startswith("*"):
                validos.append(regi1)
            buffer = gamesDat.read(2)
            registro = []

    with open('games.dat', 'wb') as gamesCompactados:
        for registro in validos:
            tam = len(registro).to_bytes(2, 'little')
            gamesCompactados.write(tam)
            gamesCompactados.write(registro)

    '''with open('games.dat', 'rb') as gamesDat2:
        buffer = gamesDat2.read(2)
        while buffer != b'':
            tam = int.from_bytes(buffer, "little")
            regi = gamesDat2.read(tam).decode()
            registro:list[str] = regi.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]
            indice = int(registro[0])
            primarioLista = [ChavePrincipal(indice, offset)] + primarioLista
            organiza_lista_chPrincipal(primarioLista)
            offset += tam + 2
            buffer = gamesDat2.read(2)

    with open("primario.ind", "wb") as primario:
        for i in primarioLista:
            linha = struct.pack(fmtPrimario, i.indice, i.offset)
            primario.write(linha) '''


def executar_operacoes(nome_arquivo):
    print(f"\n-------> Executando operações do arquivo: {nome_arquivo} <-------\n")
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:

            listas: list[list[ChavePrincipal]|list[ChaveSecundaria]|list[Indices]] = [[], [], [], []]

            with open("primario.ind", 'rb') as arq:
                listas[0] = carrega_indices(arq, 1)
            with open("genero.ind", 'rb') as arq:
                listas[1] = carrega_indices(arq, 2)
            with open("publicadora.ind", 'rb') as arq:
                listas[2] = carrega_indices(arq, 2)
            with open("listaInvertida.lst", 'rb') as arq:
                listas[3] = carrega_indices(arq, 3)
            
            games = open("games.dat", 'r+b')

            for linha in f:
                linha = linha.strip()

                if not linha:
                    continue  # pula linha vazia
                
                partes = linha.split(" ", 1)

                if len(partes) < 2:
                    continue

                operacao = partes[0]
                argumento = partes[1]

                if operacao == 'bp':
                    busca_indice_primario(listas, int(argumento), games)
                elif operacao == 'bs1':
                    busca_indice_secundario(listas, 1, str(argumento), games)
                elif operacao == 'bs2':
                    busca_indice_secundario(listas, 2, str(argumento), games)
                elif operacao == 'i':
                    listas = insercao(listas, str(argumento), games)
                elif operacao == "r":
                    listas = remocao(listas, int(argumento), games)

                else:
                    print("Comando não identificado. Por favor, verifique o arquivo de operações.")   
                print("")

            games.close()

            with open("primario.ind", "wb") as primario:
                for i in listas[0]:
                    linha = struct.pack(fmtPrimario, i.indice, i.offset)
                    primario.write(linha)

            with open("genero.ind", "wb") as genero:
                for i in listas[1]:
                    linha = struct.pack(fmtSecundario, i.nome.encode(), i.indice)
                    genero.write(linha)

            with open("publicadora.ind", "wb") as publicadora:
                for i in listas[2]:
                    linha = struct.pack(fmtSecundario, i.nome.encode(), i.indice)
                    publicadora.write(linha)

            with open("listaInvertida.lst", "wb") as listaTotal:
                for i in listas[3]:
                    linha = struct.pack(fmtInvertido, i.indice, i.proxGenero, i.proxPublicadora)
                    listaTotal.write(linha)

    except FileNotFoundError:
        print("Erro: arquivo de operações não encontrado.")


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
        construir_indices()
        
    else:
        print(f"Flag '{flag}' não reconhecida.")

if __name__ == "__main__":
    main()                                                         
