import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression, GammaRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

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

# Transformar cada UF em várias colunas, pra pegar true e false
# df['UF'].replace(to_replace=['', 'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'], value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], inplace=True)
df['UF'].replace(to_replace=['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'], value=0, inplace=True) # 0 para a região norte do país
df['UF'].replace(to_replace=['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA'], value=1, inplace=True) # 1 para a região nordeste do país
df['UF'].replace(to_replace=['MT', 'MS', 'GO', 'DF'], value=2, inplace=True) # 2 para a região centro-oeste do país
df['UF'].replace(to_replace=['SP', 'RJ', 'ES', 'MG'], value=3, inplace=True) # 3 para a região sudeste do país
df['UF'].replace(to_replace=['PR', 'RS', 'SC'], value=4, inplace=True) # 4 para a região sul do país

df['Escolaridade'].replace(to_replace=['ALFABETIZADO SEM CURSOS REGULARES', 'ENSINO FUNDAMENTAL INCOMPLETO', 'ENSINO FUNDAMENTAL', 'ENSINO MEDIO', 'ENSINO SUPERIOR', 'MESTRADO', 'DOUTORADO'], value=[0, 1, 2, 3, 4, 5, 6], inplace=True)


is_norte = []
is_nordeste = []
is_centro_oeste = []
is_sudeste = []
is_sul = []

for index, data in df.iterrows():
  data['Testando'] = True
  if data['UF'] not in [0, 1, 2, 3, 4]:
    df = df.drop(index)
  if data['UF'] == 0:
    is_norte.append(True)
    is_nordeste.append(False)
    is_centro_oeste.append(False)
    is_sudeste.append(False)
    is_sul.append(False)
  elif data['UF'] == 1:
    is_norte.append(False)
    is_nordeste.append(True)
    is_centro_oeste.append(False)
    is_sudeste.append(False)
    is_sul.append(False)
  elif data['UF'] == 2:
    is_norte.append(False)
    is_nordeste.append(False)
    is_centro_oeste.append(True)
    is_sudeste.append(False)
    is_sul.append(False)
  elif data['UF'] == 3:
    is_norte.append(False)
    is_nordeste.append(False)
    is_centro_oeste.append(False)
    is_sudeste.append(True)
    is_sul.append(False)
  elif data['UF'] == 4:
    is_norte.append(False)
    is_nordeste.append(True)
    is_centro_oeste.append(False)
    is_sudeste.append(False)
    is_sul.append(True)

df['Norte'] = is_norte
df['Nordeste'] = is_nordeste
df['Centro Oeste'] = is_centro_oeste
df['Sudeste'] = is_sudeste
df['Sul'] = is_sul

# print(df['UF'].describe())
# print(df['Escolaridade'].describe())
# print(df['Ingresso'].describe())

print(df)

X = df[['Norte', 'Nordeste', 'Centro Oeste', 'Sudeste', 'Sul', 'Ingresso', 'Escolaridade']]
y = df [['Val']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

model = GammaRegressor()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(mean_squared_error(y_test, predictions))

# plt.hist(df['Val'])
# plt.show()

# sns.regplot(y_test, predictions)
# plt.show()

# Regiao com escolaridade
testes_regiao_escolaridade = [[True, False, False, False, False, 37.759868, 0], [True, False, False, False, False, 37.759868, 1], [True, False, False, False, False, 37.759868, 2], [True, False, False, False, False, 37.759868, 3], [True, False, False, False, False, 37.759868, 4], [True, False, False, False, False, 37.759868, 5], [True, False, False, False, False, 37.759868, 6], [False, True, False, False, False, 37.759868, 0], [False, True, False, False, False, 37.759868, 1], [False, True, False, False, False, 37.759868, 2], [False, True, False, False, False, 37.759868, 3], [False, True, False, False, False, 37.759868, 4], [False, True, False, False, False, 37.759868, 5], [False, True, False, False, False, 37.759868, 6], [False, False, True, False, False, 37.759868, 0], [False, False, True, False, False, 37.759868, 1], [False, False, True, False, False, 37.759868, 2], [False, False, True, False, False, 37.759868, 3], [False, False, True, False, False, 37.759868, 4], [False, False, True, False, False, 37.759868, 5], [False, False, True, False, False, 37.759868, 6], [False, False, False, True, False, 37.759868, 0], [False, False, False, True, False, 37.759868, 1], [False, False, False, True, False, 37.759868, 2], [False, False, False, True, False, 37.759868, 3], [False, False, False, True, False, 37.759868, 4], [False, False, False, True, False, 37.759868, 5], [False, False, False, True, False, 37.759868, 6], [False, False, False, False, True, 37.759868, 0], [False, False, False, False, True, 37.759868, 1], [False, False, False, False, True, 37.759868, 2], [False, False, False, False, True, 37.759868, 3], [False, False, False, False, True, 37.759868, 4], [False, False, False, False, True, 37.759868, 5], [False, False, False, False, True, 37.759868, 6]]
predictions = model.predict(testes_regiao_escolaridade)
print(predictions)
print('\n\n\n\n\n')
plt.hist(predictions)
plt.savefig("regiao-escolaridade.png")

# Regiao com ingresso
testes_regiao_ingresso = [[True, False, False, False, False, 10.000000, 0], [True, False, False, False, False, 36.000000, 0], [True, False, False, False, False, 38.000000, 0], [True, False, False, False, False, 41.250000, 0], [True, False, False, False, False, 56.000000, 0], [False, True, False, False, False, 10.000000, 0], [False, True, False, False, False, 36.000000, 0], [False, True, False, False, False, 38.000000, 0], [False, True, False, False, False, 41.250000, 0], [False, True, False, False, False, 56.000000, 0], [False, False, True, False, False, 10.000000, 0], [False, False, True, False, False, 36.000000, 0], [False, False, True, False, False, 38.000000, 0], [False, False, True, False, False, 41.250000, 0], [False, False, True, False, False, 56.000000, 0], [False, False, False, True, False, 10.000000, 0], [False, False, False, True, False, 36.000000, 0], [False, False, False, True, False, 38.000000, 0], [False, False, False, True, False, 41.250000, 0], [False, False, False, True, False, 56.000000, 0], [False, False, False, False, True, 10.000000, 0], [False, False, False, False, True, 36.000000, 0], [False, False, False, False, True, 38.000000, 0], [False, False, False, False, True, 41.250000, 0], [False, False, False, False, True, 56.000000, 0]]
predictions = model.predict(testes_regiao_ingresso)
print(predictions)
print('\n\n\n\n\n')
plt.hist(predictions)
plt.savefig("regiao-ingresso.png")

# Ingresso com escolaridade
testes_ingresso_escolaridade = [[True, False, False, False, False, 10.000000, 0], [True, False, False, False, False, 36.000000, 0], [True, False, False, False, False, 38.000000, 0], [True, False, False, False, False, 41.250000, 0], [True, False, False, False, False, 56.000000, 0], [True, False, False, False, False, 10.000000, 1], [True, False, False, False, False, 36.000000, 1], [True, False, False, False, False, 38.000000, 1], [True, False, False, False, False, 41.250000, 1], [True, False, False, False, False, 56.000000, 1], [True, False, False, False, False, 10.000000, 2], [True, False, False, False, False, 36.000000, 2], [True, False, False, False, False, 38.000000, 2], [True, False, False, False, False, 41.250000, 2], [True, False, False, False, False, 56.000000, 2], [True, False, False, False, False, 10.000000, 3], [True, False, False, False, False, 36.000000, 3], [True, False, False, False, False, 38.000000, 3], [True, False, False, False, False, 41.250000, 3], [True, False, False, False, False, 56.000000, 3], [True, False, False, False, False, 10.000000, 4], [True, False, False, False, False, 36.000000, 4], [True, False, False, False, False, 38.000000, 4], [True, False, False, False, False, 41.250000, 4], [True, False, False, False, False, 56.000000, 4], [True, False, False, False, False, 10.000000, 5], [True, False, False, False, False, 36.000000, 5], [True, False, False, False, False, 38.000000, 5], [True, False, False, False, False, 41.250000, 5], [True, False, False, False, False, 56.000000, 5], [True, False, False, False, False, 10.000000, 6], [True, False, False, False, False, 36.000000, 6], [True, False, False, False, False, 38.000000, 6], [True, False, False, False, False, 41.250000, 6], [True, False, False, False, False, 56.000000, 6]]
predictions = model.predict(testes_ingresso_escolaridade)
print(predictions)
plt.hist(predictions)
plt.savefig("ingresso-escolaridade.png")

# Para o teste de hipótese usar a media e o desvio padrão para cada um dos casos