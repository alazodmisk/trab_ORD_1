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


#FUNÇÕES AUXILIARES
'''Funções busca_binaria_chPrincipal(argumento, lista) e busca_binaria_chSecundaria(argumento,
lista) utilizadas para encontrar a posição de um *argumento* em *lista*.
Retorna -1 caso não esteja presente'''
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


'''Funções organiza_lista_chPrincipal(lista) e organiza_lista_chSecundaria(lista) utilizadas para
organizar listas quando há inserção de uma nova chave em *lista*.
Método de Insertion Sort, analisando a posição ideal de um novo ID inserido no começo.'''
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

'''Existem dois casos de Organizacao:
- Por Genero =       organiza_prox(*idNovo*, 1, *posicaoLista*, invertidaLista, generoLista)
- Por Publicadora =  organiza_prox(*idNovo*, 2, *posicaoLista*, invertidaLista, publicadoraLista)

dessa forma temos *qualChave* para diferenciar entre organizacao por Genero (1) e por Publicadora
(2), para podermos atualizar os .prox de *invertida* e, caso o primeiro caso de uma chaveSecundaria
seja alterado, atualizar a *lista*.
Atualizações de acordo com o *idNovo* comecando por *posicaoLista* (primeiro caso de chaveSecundaria
encontrado.)'''
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

    quebra = b"\n"

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

    
##FUNÇÕES PARA CARREGAR OS .IND E PARA CARREGAR A LISTA INVERTIDA
def carrega_indice_primario(primarioLista:list[ChavePrincipal]):
    tamanho = struct.calcsize(fmtPrimario)
    with open("primario.ind", 'rb') as primario:
        linha = primario.read(tamanho)
        while len(linha) == tamanho:
            buffer = struct.unpack(fmtPrimario, linha)
            primarioLista.append(ChavePrincipal(buffer[0], buffer[1]))
            linha = primario.read(tamanho)
    return primarioLista
        
def carrega_indice_genero(generoLista:list):
    tamanho = struct.calcsize(fmtSecundario)
    with open("genero.ind", 'rb') as genero:
        linha = struct.unpack(tamanho)
        while len(linha) == tamanho:
            buffer = struct.unpack(fmtSecundario, linha)
            generoLista.append(ChaveSecundaria(buffer[0], buffer[1]))
            linha = genero.read
    return generoLista

def carrega_indice_publicadora(publicadoraLista:list):
    with open("genero.ind", 'rb') as publicadora:
        linha = struct.unpack(fmtSecundario, publicadora.read(struct.calcsize(fmtSecundario)))
        while linha != None:
            publicadoraLista.append(ChaveSecundaria(linha[0], linha[1]))
            linha = struct.unpack(fmtSecundario, publicadora.read(struct.calcsize(fmtSecundario)))
    return publicadoraLista
        
def carregar_listaInvertida(listaInvertida):
    with open("listaInvertida.lst", 'rb') as arquivo:
        linha = struct.unpack(fmtInvertido, arquivo.read(struct.calcsize(fmtInvertido)))
        while linha != None:
            listaInvertida.append(Indices(linha[0], linha[1], linha[2]))
            linha = struct.unpack(fmtInvertido, arquivo.read(struct.calcsize(fmtInvertido)))
    return listaInvertida


##FUNÇÕES AUXILIARES DA EXECUÇÃO DAS OPERAÇÕES
def busca_indice_primario(argumento: int):
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

    print("Iniciando a busca...")
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

    
    
def busca_indice_genero(argumento: str):
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


def busca_indice_publicadora(argumento: str):
    print("Iniciando a busca pelo indice secundário: publicadora...")
    primarioLista: list[ChavePrincipal] = []
    listaInvertida: list[Indices] = []
    publicadoraLista: list[ChaveSecundaria] = []

    publicadoraLista = carrega_indice_genero(publicadoraLista)
    
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
