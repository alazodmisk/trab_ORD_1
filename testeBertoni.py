import io
import sys
import struct


fmtPrimario = '<HI'
fmtSecundario = '30sB'
fmtInvertido = '<3h'


class RegistroJogo:
    def __init__(self, Tamanho:int, ID:int, Nome:str, Ano:int, Genero:str, Publicadora:str, Plataforma:str):
        self.Tamanho = Tamanho
        self.ID = ID
        self.Nome = Nome
        self.Ano = Ano
        self.Genero = Genero
        self.Publicadora = Publicadora
        self.Plataforma = Plataforma

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

            indice = int(registro[0])

            primarioLista = [ChavePrincipal(indice, offset)] + primarioLista
            organiza_lista_chPrincipal(primarioLista)
            offset += tam + 2

            finalLista = len(listaInvertida)

            #posicaoGen refere-se ao próximo caso de Genero do novo registro.
            posicaoGen = busca_binaria_chSecundaria(registro[3], generoLista)
            if posicaoGen == -1:    #Nunca antes registrado
                generoLista = [ChaveSecundaria(registro[3], finalLista)] + generoLista
                organiza_lista_chSecundaria(generoLista)
            else:
                posicaoGen = organiza_proxs(indice, 1, posicaoGen, listaInvertida, generoLista)
            
            #posicaoPubl refere-se ao próximo caso de Publicadora do novo registro.
            posicaoPubl = busca_binaria_chSecundaria(registro[4], publicadoraLista)
            if posicaoPubl == -1:   #Nunca antes registrada
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

def busca_indice_primario(argumento: int, listas:list):
    print("Iniciando a busca...")
    primarioLista:list[ChavePrincipal] = listas[0]

    pos = busca_binaria_chPrincipal(argumento, primarioLista)

    if pos != -1:
        offset = primarioLista[pos].offset

        with open("games.dat", "rb") as games:
            games.seek(offset)
            tam = int.from_bytes(games.read(2), "little")
            registro = games.read(tam).decode()
            print(registro)
    else:
        print("Registro não encontrado! <erro de argumento (índice) inválido>")

    print("=============================")

def busca_indice_genero(argumento: str, listas:list):
    print("Iniciando a busca pelo indice secundário: Gênero...")

    primarioLista: list[ChavePrincipal] = listas[0]
    generoLista: list[ChaveSecundaria] = listas[1]
    listaInvertida: list[Indices] = listas[3]

    pos = busca_binaria_chSecundaria(argumento, generoLista)

    if pos == -1:
        print("Gênero não encontrado!")
        return

    atual = generoLista[pos].indice

    while atual != -1:
        no = listaInvertida[atual]
        id_jogo = no.indice
        posPrim = busca_binaria_chPrincipal(id_jogo, primarioLista)

        if posPrim != -1:
            offset = primarioLista[posPrim].offset
            with open("games.dat", "rb") as games:
                games.seek(offset)
                tam = int.from_bytes(games.read(2), "little")
                registro = games.read(tam).decode()
                print(registro)
        atual = no.proxGenero

    print("=============================")

def busca_indice_publicadora(argumento: str, listas:list):
    print("Iniciando a busca pelo indice secundário: publicadora...")

    primarioLista: list[ChavePrincipal] = listas[0]
    publicadoraLista: list[ChaveSecundaria] = listas[2]
    listaInvertida: list[Indices] = listas[3]
    
    pos = busca_binaria_chSecundaria(argumento, publicadoraLista)

    if pos == -1:
        print("Publicadora não encontrado!")
        return
    
    atual = publicadoraLista[pos].indice

    while atual != -1:
        no = listaInvertida[atual]

        id_jogo = no.indice

        posPrim = busca_binaria_chPrincipal(id_jogo, primarioLista)

        if posPrim != -1:
            offset = primarioLista[posPrim].offset

            with open("games.dat", "rb") as games:
                games.seek(offset)
                tam = int.from_bytes(games.read(2), "little")
                registro = games.read(tam).decode()
                print(registro)
        atual = no.proxPublicadora
    
    print("=============================")


def insercao(listas: list[list], argumento: str, finalGames: int):
    registro = argumento.split('|')
    indice = int(registro[0])
    print(f'Inserção do registro de chave "{indice}" ({len(argumento)} bytes)')

    pos = busca_binaria_chPrincipal(indice, listas[0])

    if pos == -1:
        listas[0] = [ChavePrincipal(indice, finalGames + len(argumento))] + listas[0]
        organiza_lista_chPrincipal(listas[0])

        posGen = busca_binaria_chSecundaria(registro[3], listas[1])
        if posGen == -1:
            listas[1] = [ChaveSecundaria(registro[3], indice)] + listas[1]
            organiza_lista_chSecundaria(listas[1])
        else:
            posGen = organiza_proxs(indice, 1, posGen, listas[3], listas[1])
        

        posPubl = busca_binaria_chSecundaria(registro[4], listas[2])
        if posPubl == -1:
            listas[2] = [ChaveSecundaria(registro[4], indice)] + listas[2]
            organiza_lista_chSecundaria(listas[2])
        else:
            posPubl = organiza_proxs(indice, 2, posPubl, listas[3], listas[2])

        listas[3].append(Indices(indice, posGen, posPubl))

    else:
        print("Registro descartado (IDs duplicados não são aceitos).")
    
def remocao(listas: list[list], argumento: int):
    print(f'Remoção do registro de chave "{argumento}"')

    pos = busca_binaria_chPrincipal(argumento, listas[0])

    if pos != -1:
        
    else:
        print("Registro não encontrado!")

def compactar_arquivo():
    print("Iniciando a compactação do arquivo...")
    '''
    Cria uma lista pra ir colocando os válidos
    cria com o nome games_compactado.dat
    open games.dat as gamesDat
    buffer = games.read[2]
    tamanho = int.frombytes(buffer, 'little') ##Isso do primeiro registro
        Enquanto tamanho != b''  
                regi:str = buffer.decode()
                registro:list[str] = regi.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]
                for i in buffer[0] ##buffer[0] = ID
                if i == *
                    não adiciona na lista dos válidos
                tranforma os objetos da lista em objetos do tipo registroJogo (todos os campos + tamanho)
                adiciona nos válidos
                escreve o tamanho + o registro no games_compactado.dat (usando structure.pack)
                tamanho = gamesDat.read(2)
    chama a constrói indices
    '''
    validos:list[RegistroJogo]
    nomeArquivo = str(input("Digite o nome do arquivo para compactação: "))
    with open('games.dat', 'rb') as gamesDat:
        buffer = gamesDat.read(2)
        tamanho = int.from_bytes(buffer, 'little')


def executar_operacoes(nome_arquivo):
    print(f"Executando operações do arquivo: {nome_arquivo}")
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            games = open("games.dat", 'ab')
            finalGames = games.tell()

            listas: list[list[ChavePrincipal]|list[ChaveSecundaria]|list[Indices]] = [[], [], [], []]

            arq = open("primario.ind", 'rb')
            listas[0] = carrega_indices(arq, 1)
            arq.close()

            arq = open("genero.ind", 'rb')
            listas[1] = carrega_indices(arq, 2)
            arq.close()

            arq = open("publicadora.ind", 'rb')
            listas[2] = carrega_indices(arq, 2)
            arq.close()

            arq = open("listaInvertida.lst", 'rb')
            listas[3] = carrega_indices(arq, 3)
            arq.close()
            
            for linha in f:
                linha = linha.strip()

                if not linha:
                    continue  # pula linha vazia
                
                partes = linha.split(" ", 1)
                operacao = partes[0]
                argumento = partes[1]

                if operacao == 'bp':
                    busca_indice_primario(int(argumento), listas)

                elif operacao == 'bs1':
                    busca_indice_genero(str(argumento), listas)

                elif operacao == 'bs2':
                    busca_indice_publicadora(str(argumento), listas)

                elif operacao == 'i':
                    insercao(listas, str(argumento), finalGames)

                elif operacao == "r":
                    remocao(listas, int(argumento))

                else:
                    print("Comando não identificado. Por favor, verifique o arquivo de operações.")    

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
        
    else:
        print(f"Flag '{flag}' não reconhecida.")

if __name__ == "__main__":
    main()                                                         
