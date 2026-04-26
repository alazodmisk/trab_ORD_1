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
    proxPublicadora: int
    proxGenero: int




#FUNÇÕES AUXILIARES
def busca_binaria(num:int, lista:list[indicesInvertida]) -> indicesInvertida:
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





def construir_indices():
    primarioLista:list[identificador] = [identificador(0,0)]
    generoLista:list[genero] = []
    publicadoraLista:list[publicadora] = []
    listaInvertida:list[indicesInvertida] = []

    with open("games.dat", "rb") as games:
        buffer = games.read(2)
        while buffer != "+":
            tam = int.from_bytes(buffer)
            buffer = games.read(buffer)
            buffer = buffer.decode()

            registro:list = buffer.split("|") #[ID, Nome, Ano, Genero, Publicadora, Plataforma]

            indice = int(registro[0])
            primarioLista = [identificador(indice, tam)] + primarioLista
            for i in range(len(primarioLista) - 1):
                if primarioLista[i].indice > primarioLista[i+1].indice:
                    aux = primarioLista[i+1]
                    primarioLista[i+1] = primarioLista[i]
                    primarioLista[i] = aux
                else:
                    primarioLista[i+1].offset += tam

            #INCLUSAO ORDENADA NA LISTA INVERTIDA
            listaInvertida = [indicesInvertida(indice, -1, -1)] + listaInvertida
            for i in range(len(listaInvertida)):
                if listaInvertida[i].indice > listaInvertida[i+1].indice:
                    aux = listaInvertida[i]
                    listaInvertida[i] = listaInvertida[i+1]
                    listaInvertida[i+1] = aux
                else:
                    break

            #ATUALIZAÇAO DE INDICES EM RELACAO A GENERO
            jaPresente = False
            aux = registro[3]
            for i in generoLista:
                if i.nome == aux:
                    jaPresente = True
                    indice_aux = i.indice
                    break

            if jaPresente:
                while indice != -1:
                    indice = busca_binaria(indice_aux, listaInvertida).proxGenero
                listaInvertida[indice].proxGenero = indice
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
                while indice != -1:
                    indice = busca_binaria(indice_aux, listaInvertida).proxPublicadora
                listaInvertida[indice].proxPublicadora = indice
            else:
                publicadoraLista += [publicadora(aux, indice)]
            
                
                    



    print("Iniciando a construção dos índices...")
    open(games.dat)
    buffer = games.read(1)
    
    with open("primario.ind", "w+") as primario:
        primario.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos
        primario.ind[anterior], primario.ind[tamanho anterior]+buffer

    buffer = games.read(buffer)



    with open("publicadora.ind", "w+") as publicadora:
        
        publicadora.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos
        buffer2 = buffer[x,y] 
        for i in publicadora.ind:
            se achar -> pula
            se nao -> adiciona o buffer2 com seu indice primario


    with open("genero.ind", "w+") as genero:
        genero.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos
        buffer2 = buffer[x,y] 
        for i in genero.ind:
            se achar -> pula
            se nao -> adiciona o buffer2 com seu indice primario

    with open("listaInvertida.lst", "w+") as listaInvertida:
        listaInvertida.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos

    



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
