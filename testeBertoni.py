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
    def __init__(self, posicao: int, nome:str):
        self.posicao = posicao #Primeiro caso de publicadora *nome*
        self.nome = nome
        

class Genero:
    def __init__(self, posicao: int, nome:str):
        self.posicao = posicao #Primeiro caso de genero *nome*
        self.nome = nome
        

class IndicesInvertida:
    def __init__(self, indice: int, proxGenero: int, proxPublicadora: int):
        self.indice = indice
        self.proxGenero = proxGenero
        self.proxPublicadora = proxPublicadora



#FUNÇÕES AUXILIARES
def busca_binaria(num:int, lista:list[IndicesInvertida] | list[Identificador]) -> IndicesInvertida | Identificador:
    inicio = 1
    final = len(lista) - 1
    while inicio <= final:
        media = (inicio+final)//2
        if lista[media].indice == num:
            return lista[media]
        elif lista[media].indice < num:
            inicio = media + 1
        else:
            final = media - 1

    raise ValueError("Jogo não presente cenário indevido, a nome_presente() foi usada incorretamente.")


def nome_presente(nome: str, lista: list[Genero] | list[Publicadora]) -> int:
    for i in lista:
        if i.nome == nome:
            return i.posicao
    return -1

def troca(i: int, lista: list[Identificador|IndicesInvertida]) -> None:
    aux = lista[i+1]
    lista[i+1] = lista[i]
    lista[i] = aux



def construir_indices():
    primarioLista: list[Identificador] = []
    generoLista: list[Genero] = []
    publicadoraLista: list[Publicadora] = []
    listaInvertida: list[IndicesInvertida] = []
    offset: int = 0

    with open('games.dat', 'rb') as games:
        buffer = games.read(2)

        while buffer != b'':
            tam = int.from_bytes(buffer, "little")
            buffer = games.read(tam).decode()

            registro:list[str] = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]

            indice = int(registro[0])

            #primarioLista += [Identificador(indice, offset)]
            #primarioLista.sort()
            primarioLista = [Identificador(indice, offset)] + primarioLista
            for i in range(len(primarioLista) - 1):
                if primarioLista[i].indice > primarioLista[i+1].indice:
                    aux = primarioLista[i+1]
                    primarioLista[i+1] = primarioLista[i]
                    primarioLista[i] = aux
                else:
                    break

            offset += tam + 2
            finalLista = len(listaInvertida)

            #ATUALIZAÇAO DE INDICES EM RELACAO A GENERO
            posicaoGen = nome_presente(registro[3], generoLista)

            if posicaoGen == -1:
                generoLista += [Genero(finalLista, registro[3])]
            else:
                if listaInvertida[posicaoGen].indice > indice:
                    for i in generoLista:
                        if i.nome == registro[3]:
                            i.posicao = finalLista
                            break
                else:
                    while listaInvertida[posicaoGen].proxGenero != -1 and listaInvertida[listaInvertida[posicaoGen].proxGenero].indice < indice:
                        posicaoGen = listaInvertida[posicaoGen].proxGenero
                    
                    aux = listaInvertida[posicaoGen].proxGenero
                    listaInvertida[posicaoGen].proxGenero = finalLista
                    posicaoGen = aux
                

            #ATUALIZAÇAO DE INDICES EM RELACAO A PUBLICADORA
            posicaoPubl = nome_presente(registro[4], publicadoraLista) 

            if posicaoPubl == -1: #Publicadora nunca antes registrada
                publicadoraLista += [Publicadora(finalLista, registro[4])]
            else:
                if listaInvertida[posicaoPubl].indice > indice:
                    for i in publicadoraLista:
                        if i.nome == registro[4]:
                            i.posicao = finalLista
                            break
                else:
                    while listaInvertida[posicaoPubl].proxPublicadora != -1 and listaInvertida[listaInvertida[posicaoPubl].proxPublicadora].indice < indice:
                        posicaoPubl = listaInvertida[posicaoPubl].proxPublicadora
                    
                    aux = listaInvertida[posicaoPubl].proxPublicadora
                    listaInvertida[posicaoPubl].proxPublicadora = finalLista
                    posicaoPubl = aux

            listaInvertida += [IndicesInvertida(indice, posicaoGen, posicaoPubl)]

            buffer = games.read(2)


    with open("primario.ind", "w+") as primario:
        for i in primarioLista:
            linha = str(i.indice) + " " + str(i.offset)
            primario.write(linha + "\n") 

    with open("publicadora.ind", "w+") as publicadora:
        for i in publicadoraLista:
            linha = str(i.posicao) + " " + i.nome
            publicadora.write(linha + "\n") 
            
    with open("genero.ind", "w+") as genero:
        for i in generoLista:
            linha = str(i.posicao) + " " + i.nome
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
