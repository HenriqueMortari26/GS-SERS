# Otimização Energética em Cenários Híbridos: EcoWork Analytics


**GLOBAL SOLUTION - SOLUÇÕES EM ENERGIAS RENOVÁVEIS E SUSTENTÁVEIS**

| Detalhe | Informação |
| :--- | :--- |
| **Curso** | Ciências da Computação - 2º Semestre (2025) |
| **Tema Central** | Eficiência Energética e Sustentabilidade no Trabalho |
| **Opção Técnica** | Opção A — Análise de Dados |

## 1. Identificação da Equipa
* **Membro 1:** [SEU NOME COMPLETO] | **RM:** [SEU RM]
* **Membro 2:** [NOME DO COLEGA] | **RM:** [RM DO COLEGA]

---

## 2. O Problema e a Solução

### Problema (Conexão com o Futuro do Trabalho)
A transição para o trabalho híbrido (presencial e remoto) resultou numa ineficiência energética significativa. Muitos escritórios mantêm sistemas de climatização, iluminação e infraestrutura de TI operando em plena capacidade em dias de baixa ocupação, resultando em alto desperdício de kWh e impacto ambiental desnecessário.

### Solução: EcoWork Analytics
O EcoWork Analytics é um sistema de análise de dados desenvolvido em Python que quantifica este desperdício. Ele compara o consumo real do escritório com a ocupação diária, identificando o limiar de ineficiência energética.

O resultado é uma recomendação baseada em dados sobre quais dias da semana a empresa deve instituir o trabalho 100% remoto, promovendo um modelo de **trabalho inteligente**, econômico e sustentável.

---

## 3. Requisitos Técnicos e Implementação

### 3.1. Coleta e Análise de Dados
Utilizamos dados **simulados** (em formato CSV), estruturados realisticamente para representar:
1.  `dados_escritorio.csv`: Consumo de energia (kWh) vs. Ocupação (Pessoas Presentes).
2.  `dados_homeoffice.csv`: Consumo médio de equipamentos de trabalho por funcionário remoto.

### 3.2. Funcionalidades da Solução (Análise)
A lógica central do `main.py` executa as seguintes etapas:
* **Cálculo Per Capita:** Determinação do custo energético por pessoa em ambos os cenários (Escritório vs. Remoto).
* **Detecção de Desperdício:** Implementação de um algoritmo que aciona um *ALERTA* se o consumo do escritório for desproporcionalmente alto em relação à sua ocupação.
* **Visualização:** Geração de um gráfico de dupla escala (Consumo vs. Ocupação) para comprovar visualmente as ineficiências.

### 3.3. Tecnologias
| Ferramenta | Uso |
| :--- | :--- |
| **Python 3** | Linguagem de programação principal. |
| **Pandas** | Manipulação e processamento dos datasets CSV. |
| **Matplotlib** | Geração do relatório visual em formato gráfico. |
| **GitHub** | Repositório organizado da solução. |

---

## 4. Impacto e Ganhos Estimados

A análise simulada identificou que a **Sexta-feira** é o dia de maior ineficiência, devido à baixa ocupação (10 pessoas) e ao alto consumo residual (400 kWh). A otimização proposta gera os seguintes ganhos anuais:

| Métrica | Estimativa | Detalhe |
| :--- | :--- | :--- |
| **Ganhos Económicos** | R$ 14.560,00/ano | Economia anual projetada com o fechamento semanal. |
| **Ganhos Ambientais** | 2.080 kg CO2/ano | Redução da pegada de carbono (conversão aproximada). |
| **Ganhos de Usabilidade** | Clareza na tomada de decisão gerencial. |

---

## 5. Repositório e Execução

Esta seção detalha como o projeto está organizado no GitHub e como executá-lo.

### 5.1. Estrutura de Ficheiros
/ ├── main.py ├── dados_escritorio.csv ├── dados_homeoffice.csv ├── requirements.txt └── README.md


### 5.2. Instruções de Execução

1.  **Clonar o Repositório:**
    ```bash
    git clone [LINK DO REPOSITÓRIO]
    ```
2.  **Instalar Dependências:**
    ```bash
    pip install pandas matplotlib
    ```
3.  **Executar o Script:**
    ```bash
    python main.py
    ```
O script exibirá o relatório no console e salvará o gráfico de análise (`grafico_analise.png`) na pasta do projeto.
