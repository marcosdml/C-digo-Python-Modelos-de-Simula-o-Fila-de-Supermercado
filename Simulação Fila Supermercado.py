import pandas as pd
import random
from datetime import datetime, timedelta


# Função para gerar tempos aleatórios em minutos usando distribuição exponencial
def gerar_tempo_exponencial(medio):
    return round(1+random.expovariate(1 / medio), 2)

# Função para ajustar o fluxo de clientes com base no horário
def ajustar_fluxo_clientes(hora):
    if 11 <= hora <= 13:  # Entre 11:00 e 13:00
        #return round(random.uniform(3000, 5000))  # Fluxo maior
        return round(random.uniform(500, 800)) 
    elif 18 <= hora <= 20:  # Entre 18:00 e 20:00
        #return round(random.uniform(3000, 5000))
        return round(random.uniform(500, 800)) 
    else:
        #return round(random.uniform(500, 1000))
        return round(random.uniform(100, 400)) 

# Função para converter o tempo em minutos e segundos
def formatar_minutos_segundos(tempo_minutos):
    total_segundos = int(tempo_minutos * 60)
    horas, segundos_restantes = divmod(total_segundos, 3600)
    minutos, segundos = divmod(segundos_restantes, 60)
    return f"{horas:02}:{minutos:02}:{segundos:02}"

# Função para gerar múltiplos clientes em uma mesma chegada
def gerar_multiplos_clientes():
    # Definir a probabilidade de múltiplos clientes chegarem juntos (ex: 30% de chance de 2 a 3 clientes chegarem juntos)
    probabilidade = random.random()
    if probabilidade < 0.15:  # 15% de chance de mais de um cliente chegar
        return random.randint(2, 3)  # Chegada de 2 a 3 clientes
    else:
        return 1  # Chegada de 1 cliente

# Definindo uma semente para garantir reprodutibilidade
random.seed(1000)

# Parâmetros
hora_abertura = 7  # 7h da manhã
hora_fechamento = 22  # 22h (10h da noite)
total_minutos_abertura = (hora_fechamento - hora_abertura) * 60  # Total de minutos de funcionamento

# Criar o objeto datetime da hora de abertura
hora_abertura_datetime = datetime.strptime(f"{hora_abertura}:00", "%H:%M")

# Número de caixas disponíveis
n_caixas = 6

# Inicializando listas para armazenar os dados
dados = []

# Tempo em que cada caixa estará disponível
tempos_disponiveis = [0] * n_caixas

# Tempo de chegada do primeiro cliente
tempo_chegada_anterior = gerar_tempo_exponencial(20)  # Intervalo médio inicial

# Simulando os tempos para cada cliente
while True:
    # Calcular o horário atual
    hora_atual = (hora_abertura + tempo_chegada_anterior) % 24

    # Ajustar o fluxo de clientes com base no horário
    clientes_por_hora = ajustar_fluxo_clientes(hora_atual)
    intervalo_chegada_medio = 60 / clientes_por_hora if clientes_por_hora > 0 else 60  # Evitar divisão por zero

    # Tempo de chegada aleatório baseado na distribuição exponencial
    intervalo_chegada = gerar_tempo_exponencial(intervalo_chegada_medio)
    chegada = tempo_chegada_anterior + intervalo_chegada

    # Verifica se o tempo de chegada ultrapassa o horário de fechamento
    if chegada > total_minutos_abertura:
        break

    # Gerar a quantidade de clientes que chegam juntos
    clientes_simultaneos = gerar_multiplos_clientes()

    for _ in range(clientes_simultaneos):
        # Identificar o caixa disponível mais cedo
        menor_tempo_disponivel = min(tempos_disponiveis)
        caixa_id = tempos_disponiveis.index(menor_tempo_disponivel)

        # O tempo de espera será a diferença entre a chegada do cliente e o tempo que o caixa está disponível
        espera = max(0, menor_tempo_disponivel - chegada)

        # A chegada no caixa é o máximo entre o tempo de chegada e o tempo em que o caixa estará disponível
        chegada_no_caixa = chegada + espera

        # Gerar tempos de serviço no caixa
        checagem = gerar_tempo_exponencial(3.2)  # Tempo de checagem dos produtos
        pagamento_tempo = gerar_tempo_exponencial(0.8)  # Tempo de pagamento

        # Atualizar o tempo em que o caixa estará disponível
        tempos_disponiveis[caixa_id] = chegada_no_caixa + checagem + pagamento_tempo

        # Converter tempo em horário
        horario_chegada = hora_abertura_datetime + timedelta(minutes=chegada)
        horario_caixa = hora_abertura_datetime + timedelta(minutes=chegada_no_caixa)
        espera_formatada = formatar_minutos_segundos(espera)
        checagem_formatada = formatar_minutos_segundos(checagem)
        pagamento_formatado = formatar_minutos_segundos(pagamento_tempo)
        Saida = hora_abertura_datetime + timedelta(minutes=chegada_no_caixa) + timedelta(minutes=checagem) + timedelta(minutes=pagamento_tempo)

        # Adicionar os dados do cliente à lista
        dados.append([len(dados) + 1, horario_chegada.strftime("%H:%M:%S"), espera_formatada, horario_caixa.strftime("%H:%M:%S"), checagem_formatada, pagamento_formatado, Saida.strftime("%H:%M:%S"), caixa_id + 1])

    # Atualizar o tempo de chegada do próximo cliente (baseado no último cliente do grupo)
    tempo_chegada_anterior = chegada

# Criando um DataFrame com os dados e adicionando unidades
df = pd.DataFrame(dados, columns=[
    'Cliente',
    'Horário de Chegada',
    'Tempo de Espera na Fila',
    'Horário de Chegada no Caixa',
    'Tempo de Checagem dos Produtos',
    'Tempo de Pagamento',
    'Horário de Saída do Caixa',
    'Caixa'
])

# Adicionar a função de faixa horária aqui
def definir_faixa_horario(horario):
    hora = int(horario.split(':')[0])
    return f'{hora:02}:00 - {hora + 1:02}:00'

# Adicionar uma nova coluna 'Faixa Horária' com base no horário de chegada
df['Faixa Horária'] = df['Horário de Chegada'].apply(definir_faixa_horario)

# Exibindo o DataFrame atualizado com a nova coluna
print(df)


# Salvando o DataFrame atualizado em um arquivo Excel 
df.to_excel('/xxxx/xxxxx/xxxxx.xlsx', index=False, engine='openpyxl')

