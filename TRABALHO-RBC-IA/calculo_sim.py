import psycopg2
from dotenv import load_dotenv
import json

load_dotenv()

#Conexao com o banco
conexao = psycopg2.connect(database = "RBC", host ="localhost", user= "postgres", password = "1234", port = "5432")

#Funcao para calcular a similaridade global do novo caso
def similaridade_global(conexao, cur, path):
    
    #Abre o arquivo do novo_caso
    with open(path, 'r') as f:
        novo_caso = json.load(f)

    #Abre o arquivo da tabela de similaridade
    with open('similaridade.json', 'r') as f:
        similaridade = json.load(f)

    #Função auxiliar para calcular a similaridade local - Calculo do valor máximo na tabela de similaridade
    def valor_maximo(similaridade, key):
        maximo = 0
        for valor in similaridade[key]:
            if similaridade[key][valor] > maximo:
                maximo = similaridade[key][valor]
        return maximo


    #Função auxiliar para calcular a similaridade local - Calculo do valor mínimo na tabela de similaridade
    def valor_minimo(similaridade, key):
        minimo = 100
        for valor in similaridade[key]:
            if valor != "Desconhecido":
                if similaridade[key][valor] < minimo:
                    minimo = similaridade[key][valor]
        return minimo

    #Calcula a similaridade local
    def formula_similaridade_local(novo_caso, similaridade, key, antigo_caso,valor_maximo, valor_minimo):
        return 1-(abs(similaridade[key][novo_caso[key]]-antigo_caso)/(valor_maximo-valor_minimo))

    #Instancia um vetor dinamico similaridade_local que armazena todos os valores de similaridade local
    similaridade_local_dic = {}


    def similaridade_local(novo_caso, similaridade, similaridade_local_dic):
        #Key representa as chaves novo caso, que são as variáveis a serem analisadas
        for key in novo_caso:

            # Cria as chaves para o vetor dinamico similaridade_local baseado nas chaves do novo caso
            similaridade_local_dic[key] = {}
            # SELECT key FROM public.casos_casos
            cur.execute(f"SELECT {key} FROM public.casos_casospt")
            # Armazena os valores do banco de dados em um vetor
            antigo_caso_str = cur.fetchall()

            #Calcula o valor máximo e mínimo para auxiliar no calculo da similaridade local
            valor_maximo_var = valor_maximo(similaridade, key)
            valor_minimo_var = valor_minimo(similaridade, key)

            # Calculo do valor de similaridade_local de cada caso antigo com o novo caso
            for i in range(0, len(antigo_caso_str)):
                # Trata os casos de valor nulo no banco de dados como "Desconhecido"
                if antigo_caso_str[i][0] == None:
                    antigo_caso_str[i] = ("Desconhecido",)
                # Transforma o valor do caso antigo baseado na tabela de similaridade
                # O segundo [0] já que o valor retornado é uma tupla com apenas um valor ("valor",")
                antigo_caso_int = similaridade[key][antigo_caso_str[i][0]]
                # Chama a função que calcula a similaridade local e armazena o valor no vetor dinamico similaridade_local
                similaridade_local_dic[key][i+1] = (formula_similaridade_local(novo_caso, similaridade, key, antigo_caso_int, valor_maximo_var, valor_minimo_var))
        return similaridade_local_dic

    similaridade_local_dic = similaridade_local(novo_caso, similaridade, similaridade_local_dic).copy()

    # Puxa a tabela de pesos das variaveis do banco de dados
    cur.execute("SELECT * FROM public.casos_pesos")

    # Armazena os valores do banco de dados em um vetor
    pesos = cur.fetchall()


    # O calculo da similaridade global depende da similaridade local de todas as variveis de um caso
    # Então é necessário calcular a similaridade global para cada caso antigo
    # O calculo da similaridade global é feito pela soma da (similaridade local multiplicada pelo peso da variavel) divido pela soma dos pesos

    similaridade_global_dic = {}
    keys = list(similaridade_local_dic.keys())
    
    somaPesos = 0
    for i in range(0, len(pesos)):
        somaPesos += int(pesos[i][1])

    primeira_chave = keys[0]
    for i in range(0, len(similaridade_local_dic[primeira_chave])):
        somaSimilaridade = 0
        for key in novo_caso:
            for peso in pesos:
                if key == peso[0]:
                    aux = peso
                    break
            somaSimilaridade += similaridade_local_dic[key][i+1]*float(aux[1])

        similaridade_global_dic[i+1] = somaSimilaridade/somaPesos
    print(similaridade_global_dic)


    return similaridade_global_dic




    

    