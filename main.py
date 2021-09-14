import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

aposentadoria = pd.read_csv('./dataset/aposentados.012017.csv', encoding='ISO-8859-1', sep=';', index_col=False, names=['Nome', 'CPF', 'Matricula do Servidor', 'Nome do orgao', 'Sigla do orgao', 'Codigo do orgao', 'Cargo', 'Classe', 'Padrao', 'Referencia', 'Nivel', 'Tipo de Aposentadoria', 'Fundamentacao da inatividade', 'Nome diploma legal', 'Data publicacao do diploma legal', 'Ocorrencia de ingresso no servico', 'Ingresso', 'Valor do Rendimento Liquido'])

abono = pd.read_csv('./dataset/ABONOP_012017.csv', encoding='ISO-8859-1', sep=';', index_col=False, error_bad_lines=False)

aposentados_abono = pd.DataFrame()

aposentados_abono = pd.merge(aposentadoria, abono, on = "Nome", how="inner")

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

aposentados_abono['Ingresso'] = tempo

df = pd.DataFrame({'Nome': aposentados_abono['Nome'], 'UF': aposentados_abono['UF da Residência'], 'Ingresso':aposentados_abono['Ingresso'], 'Escolaridade': aposentados_abono['Nível de Escolaridade'], 'Val': aposentados_abono['Val']})

escolaridade_list = df['Escolaridade'].tolist()
escolaridade_list_nova = []

for escolaridade in escolaridade_list:
  escolaridade_list_nova.append(escolaridade.strip())

df['Escolaridade'] = escolaridade_list_nova

df['Val'] = df['Val'].dropna(how='any')

valor_list = df['Val'].tolist()
valor_list_nova = []

for valor in valor_list:
  valor_list_nova.append(float(valor.strip().replace(',', '.')))

df['Val'] = valor_list_nova

df['UF'].replace(to_replace=['', 'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'], value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], inplace=True)

df['Escolaridade'].replace(to_replace=['ALFABETIZADO SEM CURSOS REGULARES', 'DOUTORADO', 'ENSINO FUNDAMENTAL', 'ENSINO FUNDAMENTAL INCOMPLETO', 'ENSINO MEDIO', 'ENSINO SUPERIOR', 'MESTRADO'], value=[0, 1, 2, 3, 4, 5, 6], inplace=True)

for index, data in df.iterrows():
  if data['UF'] not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
    df = df.drop(index)

X = df[['UF', 'Ingresso', 'Escolaridade']]
y = df [['Val']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

model = LinearRegression()
model.fit(X_train, y_train)

# for index, uf in X_test['UF'].iteritems():
#   if uf not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
#     X_test.loc[index, 'UF'] = 0

#     # X_test.loc.__getitem__(index).__setitem__('UF', 0)
#     pass
#   # print(index, uf)

# print(X_test.groupby(X_test['UF']).size())

predictions = model.predict(X_test) # Acurácia do modelo

plt.hist(predictions)
plt.savefig("result.png")

# sns.regplot(x=y_test[:150], y=predictions[:150])