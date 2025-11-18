import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO ---
# Total de funcionários da empresa (para cálculo comparativo)
TOTAL_FUNCIONARIOS = 60 

def carregar_dados():
    """Carrega os ficheiros CSV para DataFrames."""
    try:
        df_office = pd.read_csv('data/dados_escritorio.csv')
        df_remote = pd.read_csv('data/dados_homeoffice.csv')
        return df_office, df_remote
    except FileNotFoundError:
        print("Erro: Ficheiros .csv não encontrados. Verifica o nome e a pasta.")
        return None, None

def analisar_eficiencia(df_office, custo_kwh_remoto, ocupacao_maxima=60):
    """
    Analisa se compensa manter o escritório aberto baseando-se na ocupação.
    Lógica melhorada:
    - Calcula consumo base proporcional à ocupação máxima
    - Compara consumo per capita realista
    - ocupacao_maxima: máxima ocupação esperada (padrão: 60 pessoas)
    """
    print("\n--- RELATÓRIO DE EFICIÊNCIA ENERGÉTICA ---")
    
    recomendacoes = []
    
    # Consumo base: proporcional à ocupação (mantém infraestrutura ligada)
    # Estimativa: ~1.33 kWh por pessoa (luzes, ar mínimo, sistemas)
    consumo_base_por_pessoa = 1.33
    
    for index, row in df_office.iterrows():
        dia = row['dia']
        consumo_office = row['consumo_kwh']
        ocupacao = row['pessoas_presentes']
        ar_ligado = row['ar_condicionado_ligado']
        
        if ocupacao == 0:
            # Escritório fechado - consumo deveria ser próximo de 0
            status = "FECHADO"
            if consumo_office > 10:  # Apenas alert se ainda consome muito
                print(f"{dia}: Consumo: {consumo_office}kWh | Ocupação: {ocupacao} | Status: {status} ⚠️ Consumo anormal!")
            else:
                print(f"{dia}: Consumo: {consumo_office}kWh | Ocupação: {ocupacao} | Status: {status}")
            continue
        
        # Consumo base esperado para essa ocupação
        consumo_base_esperado = ocupacao * consumo_base_por_pessoa
        
        # Consumo variável (além da infraestrutura)
        consumo_variavel = consumo_office - consumo_base_esperado
        consumo_per_capita_office = consumo_variavel / ocupacao if consumo_variavel > 0 else consumo_base_por_pessoa
        
        # Custo esperado se esses funcionários trabalhassem em casa
        # Nota: remoto não precisa de ar condicionado central, apenas equipamento
        consumo_remoto_por_pessoa = 1.2  # notebook (0.4) + monitor (0.3) + luz (0.1) + internet (0.1) + ar residencial compartilhado (0.3)
        
        # Margem de tolerância: 25% acima do remoto é aceitável
        limite_aceitavel = consumo_remoto_por_pessoa * 1.25
        
        # Verificar ineficiência
        if consumo_per_capita_office > limite_aceitavel:
            status = "INEFICIENTE ⚠️"
            recomendacoes.append(
                f"ALERTA: Na {dia}, consumo per capita ({consumo_per_capita_office:.2f}kWh) "
                f"excede limite aceitável ({limite_aceitavel:.2f}kWh) com {ocupacao} pessoas. AR: {ar_ligado}"
            )
        else:
            status = "OK"
            
        print(f"{dia}: {consumo_office:3.0f}kWh | Per Capita: {consumo_per_capita_office:.2f}kWh | Ocupação: {ocupacao:2.0f} | AR: {ar_ligado:3s} | Status: {status}")

    return recomendacoes

def gerar_graficos(df_office):
    """Gera visualização dos dados para o relatório."""
    plt.figure(figsize=(10, 6))
    
    # Gráfico de Barras: Consumo vs Ocupação
    dias = df_office['dia']
    consumo = df_office['consumo_kwh']
    ocupacao = df_office['pessoas_presentes']

    fig, ax1 = plt.subplots(figsize=(10,6))

    color = 'tab:blue'
    ax1.set_xlabel('Dia da Semana')
    ax1.set_ylabel('Consumo (kWh)', color=color)
    ax1.bar(dias, consumo, color=color, alpha=0.6, label='Energia (kWh)')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # Segundo eixo y para ocupação
    color = 'tab:red'
    ax2.set_ylabel('Pessoas Presentes', color=color)
    ax2.plot(dias, ocupacao, color=color, marker='o', linestyle='-', linewidth=2, label='Ocupação')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Análise de Sustentabilidade: Consumo Energético vs Ocupação')
    fig.tight_layout()
    plt.grid(True, axis='x')
    
    # Salvar o gráfico
    plt.savefig('grafico_analise.png')
    print("\nGráfico 'grafico_analise.png' gerado com sucesso!")
    plt.show()

def main():
    print("Iniciando EcoWork Analytics...")
    df_office, df_remote = carregar_dados()
    
    if df_office is not None:
        # 1. Calcular consumo médio de uma pessoa em casa
        # Equipamentos em home office: Notebook (0.4) + Monitor (0.3) + Luz (0.1) + Internet (0.1) = 0.9 kWh/dia
        # Ar residencial compartilhado aprox 0.3 kWh = total 1.2 kWh/dia
        consumo_pessoa_remoto = 1.2
        
        print(f"Consumo estimado por funcionário em Home Office: {consumo_pessoa_remoto:.2f} kWh/dia")
        print(f"Ocupação máxima esperada: {TOTAL_FUNCIONARIOS} pessoas\n")
        
        # 2. Executar Análise
        recomendacoes = analisar_eficiencia(df_office, consumo_pessoa_remoto, ocupacao_maxima=TOTAL_FUNCIONARIOS)
        
        # 3. Mostrar Recomendações
        print("\n--- RECOMENDAÇÕES DE SUSTENTABILIDADE ---")
        if recomendacoes:
            for rec in recomendacoes:
                print(rec)
            print("\nSUGESTÃO FINAL: Implementar Home Office seletivo nos dias com alertas reduz significativamente custos energéticos.")
        else:
            print("O uso energético do escritório está otimizado para a ocupação atual.")
            
        # 4. Gerar Gráfico
        gerar_graficos(df_office)

if __name__ == "__main__":
    main()