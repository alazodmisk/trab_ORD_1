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
    primarioLista = []
    publicadoraLista = []
    generoLista = []
    invertidaLista = []
    
    with open("primario.ind", "w+") as primario:
        primario.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos

    with open("publicadora.ind", "w+") as publicadora:
        publicadora.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos


    with open("genero.ind", "w+") as genero:
        genero.write("Conteúdo do arquivo de índice\n") ## Aqui vai uma iteração para ir adicionando as infos

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
