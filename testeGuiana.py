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



#FUNÇÕES AUXILIARES DA CONSTRUÇÃO DE INDICES
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
            
                


##FUNÇÕES AUXILIARES DA EXECUÇÃO DAS OPERAÇÕES
def busca_indice_primario():
    print("Iniciando a busca...")
    ''' abre o primario.ind
        trasnforma os elem do primario.ind em objetos e sobe no primarioLista
        iteração
            procura indice primario por meio de busca binária
            
        se achou
            verifica o byteoffsett
        se não
            fala que nao achou
            
        abre o games.dat
            faz o seek no byte offset
            imprime o registro
    '''
    i:int = 1

    try:
        with open("primario.ind", 'rb') as primario:
            buffer = primario.read()##Não sei oq por aqui hihi
            buffer = buffer.decode()
            dados:list = buffer.split(',')
            indice = identificador(dados[0], dados[1])
            primarioLista[0] = indice
            while buffer != '+':
                buffer = primario.read()##Não sei oq por aqui hihi
                buffer = buffer.decode()
                dados:list = buffer.split(',')
                indice = identificador(dados[0], dados[1])
                primarioLista[i] = indice
                i += 1
    except:
        print("Erro: Arquivo de índices primários não foi encontrado.")

    
def busca_indice_genero():
    print("Iniciando a busca pelo indice secundário: Gênero...")

def busca_indice_publicadora():
    print("Iniciando a busca pelo indice secundário: publicadora...")

def insercao():
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
                    insercao()
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

    #VERIFICA A FLAG DO COMANDO
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

