import sys


#LISTAS GLOBAIS
primarioLista: list
publicadoraLista: list
generoLista: list
listaInvertida: list


#ESTRUTURAS PARA GUARDAR AS CHAVES
class identificador:
    indice: int
    offset: int

class publicadora:
    nome: str
    indice: int #Primeiro caso de publicadora *nome*

class genero:
    nome: str
    indice: int #Primeiro caso de genero *nome*

class indicesInvertida:
    indice: int
    proxGenero: int
    proxPublicadora: int




#FUNÇÕES AUXILIARES
def busca_binaria(num:int, lista:list[indicesInvertida] | list[identificador]) -> indicesInvertida | identificador | None:
    inicio = 0
    final = len(lista)
    while inicio <= final:
        media = (inicio+final)//2
        if lista[media].indice == num:
            return lista[media]
        elif lista[media].indice >= num:
            inicio = media + 1
        else:
            final = media - 1
    return None



def construir_indices():
    primarioLista:list[identificador] = [identificador(0,0)]
    generoLista:list[genero] = []
    publicadoraLista:list[publicadora] = []
    listaInvertida:list[indicesInvertida] = []

    with open("games.dat", "rb") as games:
        buffer = games.read(2)
        while buffer != "":
            tam = int.from_bytes(buffer)
            buffer = games.read(tam).decode()

            registro:list[str] = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]

            indice = int(registro[0])
            primarioLista = [identificador(indice, tam)] + primarioLista
            for i in range(len(primarioLista) - 1):
                if primarioLista[i].indice > primarioLista[i+1].indice:
                    aux = primarioLista[i+1]
                    primarioLista[i+1] = primarioLista[i]
                    primarioLista[i] = aux
                else:
                    primarioLista[i+1].offset += tam

            #INCLUSAO COMO ELEMENTO 0 NA LISTA INVERTIDA
            listaInvertida = [indicesInvertida(indice, -1, -1)] + listaInvertida

            #ATUALIZAÇAO DE INDICES EM RELACAO A GENERO
            jaPresente = False
            aux = registro[3]
            for i in generoLista:
                if i.nome == aux:
                    jaPresente = True
                    indice_aux = i.indice
                    break

            if jaPresente:
                indice = busca_binaria(indice_aux, listaInvertida).proxGenero
                while indice != -1:
                    indice = busca_binaria(indice, listaInvertida).proxGenero
                listaInvertida[indice].proxGenero = listaInvertida[0].indice
            else:
                generoLista += [genero(aux, indice)]

            #ATUALIZAÇAO DE INDICES EM RELACAO A PUBLICADORA
            jaPresente = False
            aux = registro[4]
            for i in publicadoraLista:
                if i.nome == aux:
                    jaPresente = True
                    indice_aux = i.indice
                    break 

            if jaPresente:
                indice = busca_binaria(indice_aux, listaInvertida).proxPublicadora
                while indice != -1:
                    indice = busca_binaria(indice, listaInvertida).proxPublicadora
                listaInvertida[indice].proxPublicadora = listaInvertida[0].indice
            else:
                publicadoraLista += [publicadora(aux, indice)]


        #ORDENACAO DA LISTA INVERTIDA
        for i in range(len(listaInvertida)):
            if listaInvertida[i].indice > listaInvertida[i+1].indice:
                aux = listaInvertida[i]
                listaInvertida[i] = listaInvertida[i+1]
                listaInvertida[i+1] = aux
            else:
                break


        buffer = games.read(2)

    with open("primario.ind", "w+") as primario:
        for i in primarioLista:
            linha = str(i.indice) + " " + str(i.offset)
            primario.write(linha + "\n") 

    with open("publicadora.ind", "w+") as publicadora:
        for i in publicadoraLista:
            linha = i.nome + " " + str(i.indice)
            primario.write(linha + "\n") 
            
    with open("genero.ind", "w+") as genero:
        for i in generoLista:
            linha = i.nome + " " + str(i.indice)
            primario.write(linha + "\n") 

    with open("listaInvertida.lst", "w+") as listaInvertida:
        for i in listaInvertida:
            linha = str(i.indice) + " " + str(i.proxGenero) + " " + str(i.proxPublicadora)
            primario.write(linha + "\n") 

    

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

    #OIIIII GUIANAAAA
