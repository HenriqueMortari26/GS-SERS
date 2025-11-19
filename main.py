import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURAÇÃO E CARREGAMENTO DE DADOS ---
st.set_page_config(layout="wide", page_title="EcoWork Analytics - Dashboard Energético")

# Variáveis de Custo e Economia
CUSTO_POR_KWH = 0.75 
POTENCIAL_ECONOMIA_PERCENTUAL = 0.15 

# Função de Carregamento de Dados (Garante que os dados só carregam uma vez)
@st.cache_data
def load_data(file_path):
    """Carrega e preprocessa o dataset."""
    try:
        df = pd.read_csv(file_path)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df.set_index('Data')
        return df
    except FileNotFoundError:
        st.error(f"Erro: O ficheiro '{file_path}' não foi encontrado. Execute o 'data_generator.py' primeiro.")
        return pd.DataFrame()

df = load_data('consumo_anual_eletrodomesticos.csv')

if df.empty:
    st.stop()
    
# --- 1. VISÃO GERAL E GANHOS ---

st.title("🌱 EcoWork Analytics: Otimização Energética Doméstica")
st.header("Análise de Consumo Anual")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

# Cálculos Totais
consumo_total_anual = df['Consumo_Total_kWh'].sum()
custo_total_anual = consumo_total_anual * CUSTO_POR_KWH
economia_potencial = custo_total_anual * POTENCIAL_ECONOMIA_PERCENTUAL

col1.metric("Consumo Total (1 Ano)", f"{consumo_total_anual:,.0f} kWh")
col2.metric("Custo Total Estimado", f"R$ {custo_total_anual:,.2f}")
col3.metric("Economia Potencial (15%)", f"R$ {economia_potencial:,.2f}")
col4.metric("Dias Analisados", f"{len(df)} dias")


# --- 2. ANÁLISE DE SÉRIES TEMPORAIS (Histórico, Sazonalidade e Picos) ---

st.header("Histórico de Consumo (Sazonalidade e Picos)")

# Identificação de Picos (Outliers) - Requisito 3
media = df['Consumo_Total_kWh'].mean()
desvio_padrao = df['Consumo_Total_kWh'].std()
LIMIAR_PICO = media + 2 * desvio_padrao

picos_df = df[df['Consumo_Total_kWh'] > LIMIAR_PICO].copy()

# Gráfico de Linha do Histórico Total
fig_hist = px.line(df, 
                   y='Consumo_Total_kWh', 
                   title='Consumo Total Diário ao Longo do Ano',
                   height=400)

# Adicionar os picos ao gráfico para visualização
if not picos_df.empty:
    # Adicionando uma linha horizontal para referência do limiar
    fig_hist.add_hline(y=LIMIAR_PICO, line_dash="dash", line_color="orange", annotation_text="Limiar de Pico")
    
    fig_hist.add_trace(go.Scatter(x=picos_df.index, y=picos_df['Consumo_Total_kWh'],
                                  mode='markers', name='Pico Anormal',
                                  marker=dict(color='red', size=8)))

st.plotly_chart(fig_hist, use_container_width=True)

# Análise Sazonal (Agrupamento Mensal) - Requisito 4
consumo_mensal = df['Consumo_Total_kWh'].resample('M').mean().reset_index()
consumo_mensal['Mes'] = consumo_mensal['Data'].dt.strftime('%b/%y')

fig_sazonal = px.bar(consumo_mensal, x='Mes', y='Consumo_Total_kWh',
                     title='Média de Consumo Mensal (Variação Sazonal)',
                     text_auto='.2f',
                     height=350)
st.plotly_chart(fig_sazonal, use_container_width=True)


# --- 3. SEGMENTAÇÃO POR EQUIPAMENTO E PICO DIÁRIO ---

st.header("Consumo Segmentado por Equipamento")

col5, col6 = st.columns([1, 1.5])

# Consumo de cada equipamento (Gráfico de Pizza) - Requisito 5
equipamentos_colunas = ['PC_HomeOffice_kWh', 'Chuveiro_kWh', 'ArCondicionado_kWh', 'Geladeira_kWh', 'Outros_kWh']
equipamentos_consumo = df[equipamentos_colunas].sum()
equipamentos_consumo_df = equipamentos_consumo.reset_index()
equipamentos_consumo_df.columns = ['Equipamento', 'Consumo (kWh)']

fig_pizza = px.pie(equipamentos_consumo_df, values='Consumo (kWh)', names='Equipamento',
                   title='Participação Percentual no Consumo Anual',
                   hole=.3)
col5.plotly_chart(fig_pizza, use_container_width=True)


# Sugestões de Otimização (Requisito 7)
col6.subheader("Sugestões de Otimização por Horário (Segmentação)")

# Lógica de Sugestão Horária (Baseada na simulação de consumo do chuveiro)
pico_chuveiro_diario = df['Chuveiro_kWh'].mean()

if pico_chuveiro_diario > 4.5: 
    col6.markdown(f"""
    **Ação:** Evitar o uso do Chuveiro/Aquecedor das **19:00h às 21:00h** (Horário de Pico da Residência).
    
    * **Justificativa:** O consumo médio do chuveiro é elevado ({pico_chuveiro_diario:.2f} kWh/dia) e concentrado no início da noite, contribuindo para o maior pico de demanda.
    * **Impacto:** Distribuir este consumo para horários de menor demanda (após as 21:00h ou pela manhã) reduz o custo operacional e a sobrecarga.
    """)
    # Adicionar sugestão para AC
    ac_medio = df['ArCondicionado_kWh'].mean()
    if ac_medio > 1.0:
         col6.markdown(f"**Sugestão Secundária:** Se o uso do AC ({ac_medio:.2f} kWh/dia) é alto, programe-o para desligar 30 minutos antes de sair de casa, aproveitando a inércia térmica.")
else:
    col6.success("O uso de Chuveiro está eficiente. Focar na redução de outros aparelhos.")

# --- 4. ECONOMIA RETROATIVA (Requisito 6) ---

st.header("Simulação de Economia Retroativa")
st.markdown("---")

# Calcular economia se 50% dos picos tivessem sido evitados
if not picos_df.empty:
    economia_picos = (picos_df['Consumo_Total_kWh'] - LIMIAR_PICO).sum() * 0.5 * CUSTO_POR_KWH

    st.markdown(f"""
    Se você tivesse ajustado o uso nos **{len(picos_df)} dias de pico** identificados, 
    reduzindo o excesso de consumo em 50%, a economia retroativa seria de **R$ {economia_picos:,.2f}** no último ano. 
    Isto demonstra o potencial de otimização da sua rotina.
    """)
else:
    st.info("Nenhuma economia retroativa calculada, pois não foram identificados picos anormais nos dados.")

# Comando para execução
# st.code('streamlit run main.py')