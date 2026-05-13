
import sys
'''NÃO ESTÁ PRONTO AINDA'''


def compactar_arquivo():
    print("Iniciando a compactação do arquivo...")

def busca_indice_primario(argumento: int):
    print("Iniciando a busca...")
    print(argumento)
    print("===========")

def busca_indice_publicadora(argumento: str):
    print("Iniciando a busca pelo indice secundário: publicadora...")
    print(argumento)
    print("===========")

def busca_indice_genero(argumento: str):
    print("Iniciando a busca pelo indice secundário: Gênero...")
    print(argumento)
    print("===========")

def construir_indices():
    print("Construindo indices")
    print("===========")

def insercao(argumento: str):
    print("inserindo")
    print(argumento)
    print("===========")

def remocao(argumento: str):
    print("removendo")
    print(argumento)
    print("===========")



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
                    busca_indice_primario(argumento)
                elif operacao == 'bs1':
                    busca_indice_genero(argumento)
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
