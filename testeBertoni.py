import sys
import struct

fmtPrimario = '<HI'
fmtSecundario = '30sB'
fmtInvertido = '3h'


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
            
            listaInvertida.append(Indices(indice, posicaoGen, posicaoPubl))
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

    
def carrega_indice_primario(primarioLista:list[ChavePrincipal]):
    tamanho = struct.calcsize(fmtPrimario)
    with open("primario.ind", 'rb') as primario:
        linha = primario.read(tamanho)
        while len(linha) == tamanho:
            buffer = struct.unpack(fmtPrimario, linha)
            primarioLista.append(ChavePrincipal(buffer[0], buffer[1]))
            linha = primario.read(tamanho)
    return primarioLista
        
def carrega_indice_genero(generoLista:list[ChaveSecundaria]):
    tamanho = struct.calcsize(fmtSecundario)
    with open("genero.ind", 'rb') as genero:
        linha = genero.read(tamanho)
        while len(linha) == tamanho:
            buffer = struct.unpack(fmtSecundario, linha)
            nome = buffer[0].decode().strip('\x00')
            generoLista.append(ChaveSecundaria(nome, buffer[1]))
            linha = genero.read(tamanho)
    return generoLista

def carrega_indice_publicadora(publicadoraLista:list[ChaveSecundaria]):
    tamanho = struct.calcsize(fmtSecundario)
    with open("publicadora.ind", 'rb') as publicadora:
        linha = publicadora.read(tamanho)
        while len(linha) == tamanho:
            buffer = struct.unpack(fmtSecundario, linha)
            nome = buffer[0].decode().strip('\x00')
            publicadoraLista.append(ChaveSecundaria(nome, buffer[1]))
            linha = publicadora.read(tamanho)
    return publicadoraLista
        
def carregar_listaInvertida(listaInvertida:list[Indices]):
    tamanho = struct.calcsize(fmtInvertido)
    with open("listaInvertida.lst", 'rb') as arquivo:
        linha = arquivo.read(tamanho)
        while len(linha) == tamanho:
            buffer = struct.unpack(fmtInvertido, linha)
            listaInvertida.append(Indices(buffer[0], buffer[1], buffer[2]))
            linha = arquivo.read(tamanho)
    return listaInvertida


def busca_indice_primario(argumento: int):
    primarioLista: list[ChavePrincipal] = []
    primarioLista = carrega_indice_primario(primarioLista)

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

    

    '''Função busca_indice_genero(argumento) utilizada para buscar todos os registros
    de jogos que possuem um determinado gênero, com base no índice secundário
    "genero.ind" e na lista invertida "listaInvertida.lst".

    A função realiza os seguintes passos:
        - Carrega o índice secundário de gêneros para uma lista de objetos
        ChaveSecundaria.
        - Realiza busca binária para encontrar o gênero desejado.
        - Caso encontrado, obtém o índice inicial da lista invertida.
        - Percorre a lista encadeada utilizando o campo proxGenero.
        - Para cada índice primário encontrado:
            - Realiza busca no índice primário para obter o offset.
            - Acessa o arquivo "games.dat" com seek.
            - Lê e imprime o registro correspondente.

    Caso o gênero não seja encontrado, a função informa ao usuário.

    Parâmetro:
        - argumento: nome do gênero a ser buscado (string)

    Não retorna valores, apenas imprime os registros encontrados.'''

def busca_indice_genero(argumento: str):
    print("Iniciando a busca pelo indice secundário: Gênero...")

    primarioLista: list[ChavePrincipal] = []
    listaInvertida: list[Indices] = []
    generoLista: list[ChaveSecundaria] = []

    generoLista = carrega_indice_genero(generoLista)

    pos = busca_binaria_chSecundaria(argumento, generoLista)

    if pos == -1:
        print("Gênero não encontrado!")
        return

    listaInvertida = carregar_listaInvertida(listaInvertida)
    primarioLista = carrega_indice_primario(primarioLista)
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

def busca_indice_publicadora(argumento: str):
    print("Iniciando a busca pelo indice secundário: publicadora...")
    primarioLista: list[ChavePrincipal] = []
    listaInvertida: list[Indices] = []
    publicadoraLista: list[ChaveSecundaria] = []

    publicadoraLista = carrega_indice_publicadora(publicadoraLista)
    
    pos = busca_binaria_chSecundaria(argumento, publicadoraLista)

    if pos == -1:
        print("Publicadora não encontrado!")
        return

    listaInvertida = carregar_listaInvertida(listaInvertida)
    primarioLista = carrega_indice_primario(primarioLista)
    
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


def insercao(argumento: str):
    primarioLista: list[ChavePrincipal] = []
    
    registro = argumento.split('|')
    indice = int(registro[0])
    print(f'Inserção do registro de chave "{indice}"')

    primarioLista = carrega_indice_primario(primarioLista)
    pos = busca_binaria_chPrincipal(indice, primarioLista)
    if pos == -1:
        listaInvertida: list[Indices] = []
        listaInvertida = carregar_listaInvertida(listaInvertida)
        alteraInvertida = False


        generoLista: list[ChaveSecundaria] = []
        publicadoraLista: list[ChaveSecundaria] = []

        generoLista = carrega_indice_genero(generoLista)
        posGen = busca_binaria_chSecundaria(registro[3], generoLista)
        if posGen == -1:
            generoLista = [ChaveSecundaria(registro[3], indice)] + generoLista
            organiza_lista_chSecundaria(generoLista)
            
            with open("genero.ind", "wb") as genero:
                for i in generoLista:
                    linha = struct.pack(fmtSecundario, i.nome.encode(), i.indice)
                    genero.write(linha) 
        else:
            alteraInvertida = True
            posGen = organiza_proxs(indice, 1, posGen, listaInvertida, generoLista)
        

        publicadoraLista = carrega_indice_publicadora(publicadoraLista)
        posPubl = busca_binaria_chSecundaria(registro[4], publicadoraLista)
        if posPubl == -1:
            publicadoraLista = [ChaveSecundaria(registro[4], indice)] + publicadoraLista
            organiza_lista_chSecundaria(publicadoraLista)
            with open("publicadora.ind", "wb") as publicadora:
                for i in publicadoraLista:
                    linha = struct.pack(fmtSecundario, i.nome.encode(), i.indice)
                    publicadora.write(linha) 
        else:
            alteraInvertida = True
            posPubl = organiza_proxs(indice, 2, posPubl, listaInvertida, publicadoraLista)


        if alteraInvertida:
            listaInvertida.append(Indices(indice, posGen, posPubl))
            with open("listaInvertida.lst", "wb") as listaTotal:
                for j in listaInvertida:
                    linha = struct.pack(fmtInvertido, j.indice, j.proxGenero, j.proxPublicadora)
                    listaTotal.write(linha)  

        else:
            with open("listaInvertida.lst", "wb") as listaTotal:
                listaTotal.seek(len(listaTotal))
            tamanho = len(argumento)


    else:
        print("Registro descartado (IDs duplicados não são aceitos).")
      

def remocao():
    print("Iniciando a remoção...")



#AQUI TEM QUE ARRUMAR A ENTRADA PRA ACHAR AS OPERAÇÕES:
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
                    busca_indice_primario(int(argumento))
                elif operacao == 'bs1':
                    busca_indice_genero(str(argumento))
                elif operacao == 'bs2':
                    busca_indice_publicadora(argumento)
                elif operacao == 'i':
                    insercao(argumento)
                elif operacao == "r":
                    remocao(argumento)
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
