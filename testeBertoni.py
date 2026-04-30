import sys

#LISTAS GLOBAIS
primarioLista: list
publicadoraLista: list
generoLista: list
listaInvertida: list


#ESTRUTURAS PARA GUARDAR AS CHAVES
class Identificador:
    def __init__(self, indice: int, offset: int):
        self.indice = indice
        self.offset = offset

class Publicadora:
    def __init__(self, nome:str, indice: int):
        self.nome = nome
        self.indice = indice #Primeiro caso de publicadora *nome*

class Genero:
    def __init__(self, nome:str, indice: int):
        self.nome = nome
        self.indice = indice #Primeiro caso de genero *nome*

class IndicesInvertida:
    def __init__(self, indice: int, proxGenero: int, proxPublicadora: int):
        self.indice = indice
        self.proxGenero = proxGenero
        self.proxPublicadora = proxPublicadora



#FUNÇÕES AUXILIARES
def busca_binaria(num:int, lista:list[IndicesInvertida] | list[Identificador]) -> IndicesInvertida | Identificador | None:
    inicio = 1
    final = len(lista) - 1
    print(num)
    while inicio <= final:
        media = (inicio+final)//2
        print(f"{inicio} + {final} = {media} < {len(lista)}")
        if lista[media].indice == num:
            return lista[media]
        elif lista[media].indice > num:
            inicio = media + 1
        else:
            final = media - 1
    return None


def nome_presente(nome: str, lista: list[Genero] | list[Publicadora]) -> int:
    for i in lista:
        if i.nome == nome:
            return i.indice
    return -1

def troca(i: int, lista: list[Identificador|IndicesInvertida]) -> None:
    aux = lista[i+1]
    lista[i+1] = lista[i]
    lista[i] = aux


def construir_indices():
    primarioLista:list[Identificador] = [Identificador(-1,0)]
    generoLista:list[Genero] = []
    publicadoraLista:list[Publicadora] = []
    listaInvertida:list[IndicesInvertida] = []

    with open('games.dat', 'rb') as games:
        buffer = games.read(1)
        games.read(1)
        while buffer != b'':
            tam = int.from_bytes(buffer)
            buffer = games.read(tam)
            buffer = buffer.decode()

            registro:list[str] = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]

            indice = int(registro[0])                                                                                                                                                                                                                               
            primarioLista = [Identificador(indice, tam)] + primarioLista
            for i in range(len(primarioLista) - 1):
                if primarioLista[i].indice > primarioLista[i+1].indice:
                    troca(i, primarioLista)
                else:                       
                    primarioLista[i+1].offset += tam


            #INCLUSAO COMO ELEMENTO 0 NA LISTA INVERTIDA
            listaInvertida = listaInvertida + [IndicesInvertida(indice, -1, -1)]


            #ATUALIZAÇAO DE INDICES EM RELACAO A GENERO
            indiceGen = nome_presente(registro[3], generoLista) #Primeira aparição do Gênero entre os jogos
            print(f"Primeiro: {indiceGen}")

            if indiceGen != -1: # Ir para o último caso do Gênero
                indiceGen = busca_binaria(indiceGen, listaInvertida).proxGenero
                while listaInvertida[indiceGen].proxGenero > -1:
                    print(indiceGen)
                    indiceGen = busca_binaria(indiceGen, listaInvertida).proxGenero
                listaInvertida[indiceGen].proxGenero = indice
            else: #Gênero nunca antes registrado
                generoLista = generoLista + [Genero(registro[3], indice)]


            #ATUALIZAÇAO DE INDICES EM RELACAO A PUBLICADORA
            indicePubl = nome_presente(registro[4], publicadoraLista) #Primeira aparição da Publicadora entre os jogos
            print(f"Primeira: {indicePubl}")

            if indicePubl != -1: #Ir para o último caso da Publicadora 
                indicePubl = busca_binaria(indicePubl, listaInvertida).proxPublicadora
                while listaInvertida[indicePubl].proxPublicadora > -1:
                    print(indicePubl)
                    indicePubl = busca_binaria(indicePubl, listaInvertida).proxPublicadora
                listaInvertida[indicePubl].proxPublicadora = indice
            else: #Publicadora nunca antes registrada
                publicadoraLista = publicadoraLista + [Publicadora(registro[4], indice)]
            

            print(f"{listaInvertida[0].proxGenero} and {listaInvertida[0].proxPublicadora}")
            print()
            #ORDENACAO DA LISTA INVERTIDA
            for i in range(len(listaInvertida)-1):
                if listaInvertida[i].indice > listaInvertida[i+1].indice:
                    troca(i, listaInvertida)
                else:
                    break

            buffer = games.read(1)
            games.read(1)

    with open("primario.ind", "w+") as primario:
        for i in primarioLista:
            linha = str(i.indice) + " " + str(i.offset)
            primario.write(linha + "\n") 

    with open("publicadora.ind", "w+") as publicadora:
        for i in publicadoraLista:
            linha = i.nome + " " + str(i.indice)
            publicadora.write(linha + "\n") 
            
    with open("genero.ind", "w+") as genero:
        for i in generoLista:
            linha = i.nome + " " + str(i.indice)
            genero.write(linha + "\n") 

    with open("listaInvertida.lst", "w+") as listaTotal:
        for i in listaInvertida:
            linha = str(i.indice) + " " + str(i.proxGenero) + " " + str(i.proxPublicadora)
            listaTotal.write(linha + "\n") 

    

def executar_operacoes(nome_arquivo):
    print(f"Executando operações do arquivo: {nome_arquivo}")



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
