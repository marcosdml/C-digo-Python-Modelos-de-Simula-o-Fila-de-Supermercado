import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo Excel gerado através do código de simulação do modelo
dfx = pd.read_excel('/xxxx/xxxxx/xxxxx.xlsx')

# Converter colunas de tempo para minutos
dfx['Tempo de Espera na Fila'] = round(pd.to_timedelta(dfx['Tempo de Espera na Fila']).dt.total_seconds() / 60,2)
dfx['Tempo de Checagem dos Produtos'] = round(pd.to_timedelta(dfx['Tempo de Checagem dos Produtos']).dt.total_seconds() / 60,2)
dfx['Tempo de Pagamento'] = round(pd.to_timedelta(dfx['Tempo de Pagamento']).dt.total_seconds() / 60,2)

# Criar uma coluna com o tempo total de atendimento
dfx['Tempo de Atendimento'] = dfx['Tempo de Checagem dos Produtos'] + dfx['Tempo de Pagamento']

# Cálculo dos indicadores da teoria de filas

# 1. Taxa de chegada (λ)
total_clientes = len(dfx)
horario_inicio = pd.to_datetime(dfx['Horário de Chegada'].min(), format='%H:%M:%S')
horario_fim = pd.to_datetime(dfx['Horário de Chegada'].max(), format='%H:%M:%S')
total_tempo_simulado_minutos = (horario_fim - horario_inicio).total_seconds() / 60  # em minutos
lambda_chegada = total_clientes / total_tempo_simulado_minutos  # clientes por minuto

# 2. Taxa de atendimento (μ)
tempo_medio_atendimento = dfx['Tempo de Atendimento'].mean()  # tempo médio de atendimento em minutos
mi_atendimento = 1 / tempo_medio_atendimento  # clientes atendidos por minuto

# 3. Número médio de clientes no sistema (L)
L = lambda_chegada * tempo_medio_atendimento

# 4. Tempo médio no sistema (W)
W = L / lambda_chegada

# 5. Número médio de clientes na fila (Lq)
Lq = L - (lambda_chegada / mi_atendimento)

# 6. Tempo médio de espera na fila (Wq)
Wq = Lq / lambda_chegada

# 7. Fator de utilização (ρ)
n_caixas = dfx['Caixa'].nunique()
rho = lambda_chegada / (mi_atendimento * n_caixas)

# Exibir os resultados
print(f"Taxa de chegada (λ): {lambda_chegada:.2f} clientes por minuto")
print(f"Taxa de atendimento (μ): {mi_atendimento:.2f} clientes por minuto")
print(f"Número médio de clientes na fila (Lq): {Lq:.2f} clientes")
print(f"Tempo médio de espera na fila (Wq): {Wq:.2f} minutos")
print(f"Número médio de clientes no sistema (L): {L:.2f} clientes")
print(f"Tempo médio no sistema (W): {W:.2f} minutos")
print(f"Fator de utilização (ρ): {rho:.2%}")

# Gráficos de dispersão

# Gráfico 1: Dispersão do Tempo de Espera na Fila vs. Clientes
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Cliente', y='Tempo de Espera na Fila', data=dfx, palette='coolwarm', s=100)
plt.title('Tempo de Espera na Fila vs. Número de Clientes', fontsize=15)
plt.xlabel('Cliente', fontsize=12)
plt.ylabel('Tempo de Espera na Fila (min)', fontsize=12)
plt.show()

# Gráfico 2: Dispersão do Tempo de Atendimento vs. Caixa
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Caixa', y='Tempo de Atendimento', data=dfx, palette='viridis', s=100)
plt.title('Tempo de Atendimento vs. Caixa', fontsize=15)
plt.xlabel('Caixa', fontsize=12)
plt.ylabel('Tempo de Atendimento (min)', fontsize=12)
plt.show()

# Gráfico 3: Dispersão do Número de Clientes por Faixa Horária
plt.figure(figsize=(10, 6))
sns.countplot(x='Faixa Horária', data=dfx, palette='plasma')
plt.title('Número de Clientes por Faixa Horária', fontsize=15)
plt.xlabel('Faixa Horária', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.xticks(rotation=90)
plt.show()

