import pandas as pd
import matplotlib.pyplot as plt

aposentadoria = pd.read_csv('./dataset/aposentados.012017.csv', encoding='ISO-8859-1', sep=';', index_col=False, names=['Nome', 'CPF', 'Matricula do Servidor', 'Nome do orgao', 'Sigla do orgao', 'Codigo do orgao', 'Cargo', 'Classe', 'Padrao', 'Referencia', 'Nivel', 'Tipo de Aposentadoria', 'Fundamentacao da inatividade', 'Nome diploma legal', 'Data publicacao do diploma legal', 'Ocorrencia de ingresso no servico', 'Ingresso', 'Valor do Rendimento Liquido'])
abono = pd.read_csv('./dataset/ABONOP_012017.csv', encoding='ISO-8859-1', sep=';', index_col=False, error_bad_lines=False)

##aposentados_set = set()
aposentados_abono = pd.DataFrame()

aposentados_abono = pd.merge(aposentadoria, abono, on = "Nome", how="inner")

# for index_aposentadoria, dados_aposentadoria in aposentadoria.iterrows():
#   aposentados_set.add(dados_aposentadoria['Nome'])

# for index_abono, dados_abono in abono.iterrows():
#   if dados_abono['Nome'] in aposentados_set:
#     aposentados_abono = aposentados_abono.append({'Nome': dados_abono['Nome'], 'Nível de Escolaridade': dados_abono['Nível de Escolaridade'], 'UF da Residência': dados_abono['UF da Residência']}, ignore_index = True)
#     pass

ingresso = []
ingresso = aposentados_abono['Ingresso'].tolist()
tempo = []

for index in range(0, len(ingresso)):
  ano = int(ingresso[index])
  x = [int(a) for a in str(ano)]
  x = x[-4:]

  strings = [str(integer) for integer in x]
  a_string = "".join(strings)
  an_integer = int(a_string)
  tempo.insert(index, 2021 - an_integer)

print(tempo)

# print(aposentados_abono['Ingresso'])

# # Nivel de escolaridade, UF, Ingresso no servico publico
# # print(aposentadoria.groupby(['Data de ocorrencia de ingresso no servico publico']).size())
# print(aposentados_abono.groupby(['Nível de Escolaridade']).size())
# escolaridade_agrupada = aposentados_abono.groupby(['Nível de Escolaridade']).size()
# escolaridade_agrupada.plot.bar()
# plt.show()