import pandas as pd
import numpy as np
from datetime import timedelta

# --- 1. CONFIGURAÇÕES ---
# 365 dias de dados (1 ano)
N_DIAS = 365
DATA_INICIAL = pd.to_datetime('2024-01-01')

# Consumo médio base em kWh (para cada aparelho por dia)
BASE_CONSUMO = {
    'Geladeira_kWh': 1.5,
    'PC_HomeOffice_kWh': 1.2,  # Consistente, exceto em fins de semana
    'Chuveiro_kWh': 4.0,       # Alta variação sazonal
    'ArCondicionado_kWh': 0.8,  # Alta variação sazonal
    'Outros_kWh': 0.5
}

# --- 2. GERAÇÃO DA SÉRIE TEMPORAL ---
datas = [DATA_INICIAL + timedelta(days=i) for i in range(N_DIAS)]
df = pd.DataFrame({'Data': datas})

# Extrair informações de tempo
df['Dia_Semana'] = df['Data'].dt.day_name()
df['Mes'] = df['Data'].dt.month

# --- 3. APLICAÇÃO DA LÓGICA DE CONSUMO SAZONAL E DIÁRIO ---

def gerar_consumo(base, mes, dia_semana):
    """Aplica ruído e lógica sazonal/diária ao consumo base."""
    # 1. Ruído aleatório (±15% da base)
    consumo = base + np.random.uniform(-0.15 * base, 0.15 * base)
    
    # 2. Lógica Sazonal/Diária
    
    # CHUVEIRO/AQUECIMENTO (Picos no Inverno: Junho a Setembro)
    if 'Chuveiro' in nome and (mes >= 6 and mes <= 9):
        consumo *= np.random.uniform(1.2, 1.6) # Aumenta 20% a 60% no Inverno
        
    # AR CONDICIONADO (Picos no Verão: Dezembro a Março)
    elif 'ArCondicionado' in nome and (mes >= 12 or mes <= 3):
        consumo *= np.random.uniform(1.5, 2.5) # Aumenta 50% a 150% no Verão
        
    # PC HOME OFFICE (Redução no Fim de Semana)
    elif 'PC_HomeOffice' in nome and (dia_semana == 'Saturday' or dia_semana == 'Sunday'):
        consumo *= np.random.uniform(0.1, 0.4) # Reduz 60% a 90% no fim de semana
        
    # Geladeira/Outros (Consistente)
    else:
        pass
        
    # Simular picos esporádicos (Outliers)
    if np.random.rand() < 0.03: # 3% de chance de um pico anormal
         consumo *= 3.0 # Triplica o consumo para detecção de anomalias

    return max(0, consumo) # Garante que o valor não é negativo

# Aplicar a função para cada coluna de eletrodoméstico
for nome, base in BASE_CONSUMO.items():
    df[nome] = df.apply(
        lambda row: gerar_consumo(base, row['Mes'], row['Dia_Semana']), 
        axis=1
    )

# --- 4. CÁLCULO FINAL E SAÍDA ---
# Calcular Consumo Total
df['Consumo_Total_kWh'] = df[[
    'Geladeira_kWh', 'PC_HomeOffice_kWh', 'Chuveiro_kWh', 
    'ArCondicionado_kWh', 'Outros_kWh'
]].sum(axis=1)

# Renomear Dia da Semana para PT (opcional)
dias_pt = {
    'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta', 
    'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}
df['Dia_Semana'] = df['Dia_Semana'].map(dias_pt)

# Selecionar e ordenar as colunas finais
df_final = df[[
    'Data', 'Dia_Semana', 'Mes', 
    'Consumo_Total_kWh', 'PC_HomeOffice_kWh', 
    'Chuveiro_kWh', 'ArCondicionado_kWh', 
    'Geladeira_kWh', 'Outros_kWh'
]]

# Salvar o ficheiro
df_final.to_csv('consumo_anual_eletrodomesticos.csv', index=False, float_format='%.2f')
print("Ficheiro 'consumo_anual_eletrodomesticos.csv' gerado com sucesso (365 dias).")