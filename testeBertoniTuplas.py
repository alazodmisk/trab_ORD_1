import sys


#FUNÇÕES AUXILIARES
def busca_binaria(procurado: int|str, lista:list[tuple]) -> int:
    inicio = 0
    final = len(lista) - 1
    while inicio <= final:
        media = (inicio+final)//2
        if lista[media][0] == procurado:
            return media
        elif lista[media][0] < procurado:
            inicio = media + 1
        else:
            final = media - 1
    return -1

def organiza_proxs(idnovo: int, novo: str, invertida: list[tuple], lista: list[tuple], i) -> int:
    indiceLista = busca_binaria(novo, lista)
    posicao = len(invertida)
    
    indiceInvertida = lista[indiceLista][1]
    if invertida[indiceInvertida][0] > idnovo:
        lista[indiceLista] = (lista[indiceLista][0],posicao)
    else:
        while invertida[indiceInvertida][i] != -1 and invertida[invertida[indiceInvertida][i]][i] < idnovo:
            indiceInvertida = invertida[indiceInvertida][i]
        
        aux = invertida[indiceInvertida][i]
        if i == 1:
            invertida[indiceInvertida] = (invertida[indiceInvertida][0], posicao, invertida[indiceInvertida][2])
        else:
            invertida[indiceInvertida] = (invertida[indiceInvertida][0], invertida[indiceInvertida][2], posicao)
        indiceInvertida = aux

    return indiceInvertida

def organiza_lista(lista: list[tuple]) -> None:
    for i in range(len(lista)-1):
        if lista[i][0] > lista[i+1][0]:
            aux = lista[i+1]
            lista[i+1] = lista[i]
            lista[i] = aux
        else:
            break

def construir_indices():
    primarioLista: list[tuple] = []
    generoLista: list[tuple] = []
    publicadoraLista: list[tuple] = []
    listaInvertida: list[tuple] = []
    offset: int = 0

    with open('games.dat', 'rb') as games:
        buffer = games.read(2)
        while buffer != b'':
            tam = int.from_bytes(buffer, "little")
            buffer = games.read(tam).decode()

            registro:list[str] = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]
            indice = int(registro[0])

            primarioLista = [(indice, offset)] + primarioLista
            organiza_lista(primarioLista)
            offset += tam + 2


            posicaoGen = busca_binaria(registro[3], generoLista)
            if posicaoGen == -1:
                generoLista = [(registro[3], len(listaInvertida))] + generoLista #adiciona novo genero em primeiro
                organiza_lista(generoLista)
            else:
                posicaoGen = organiza_proxs(indice, registro[3], listaInvertida, generoLista, 1)


            posicaoPubl = busca_binaria(registro[4], publicadoraLista)
            if posicaoPubl == -1:
                publicadoraLista = [(registro[4], len(listaInvertida))] + publicadoraLista #adiciona nova publicadora em primeiro
                organiza_lista(publicadoraLista)
            else:
                posicaoPubl = organiza_proxs(indice, registro[4], listaInvertida, publicadoraLista, 2)

            listaInvertida += [(indice, posicaoGen, posicaoPubl)]

            buffer = games.read(2)

    with open("primario.ind", "w+") as primario:
        for i in primarioLista:
            linha = str(i[0]) + " " + str(i[1])
            primario.write(linha + "\n") 

    with open("publicadora.ind", "w+") as publicadora:
        for i in publicadoraLista:
            linha = i[0] + " " + str(i[1])
            publicadora.write(linha + "\n") 
            
    with open("genero.ind", "w+") as genero:
        for i in generoLista:
            linha = i[0] + " " + str(i[1])
            genero.write(linha + "\n") 

    with open("listaInvertida.lst", "w+") as listaTotal:
        for i in listaInvertida:
            linha = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
            listaTotal.write(linha + "\n") 


##FUNÇÕES AUXILIARES DA EXECUÇÃO DAS OPERAÇÕES
def busca_indice_primario():
    print("Iniciando a busca...")
    
def busca_indice_genero():
    print("Iniciando a busca pelo indice secundário: Gênero...")

def busca_indice_publicadora():
    print("Iniciando a busca pelo indice secundário: publicadora...")

def insercao(argumento: str):
    print("Iniciando a inserção...")

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
