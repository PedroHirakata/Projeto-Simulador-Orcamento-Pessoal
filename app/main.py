import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
from datetime import datetime

# Funções para salvar e carregar dados
def salvar_dados(dados, arquivo='data/orcamentos.json'):
    with open(arquivo, 'w') as file:
        json.dump(dados, file, indent=4)

def carregar_dados(arquivo='data/orcamentos.json'):
    try:
        with open(arquivo, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para calcular saldo
def calcular_saldo(renda, despesas):
    return renda - sum(despesas.values())

# Função principal
def main():
    st.title("Simulador de Orçamento Pessoal")

    # Carregar dados existentes
    orcamentos = carregar_dados()

    # Sidebar para navegação
    st.sidebar.title("Navegação")
    opcao = st.sidebar.radio("Escolha uma opção:", ["Novo Orçamento", "Análise e Metas", "Gerenciar Orçamentos"])

    if opcao == "Novo Orçamento":
        st.header("Novo Orçamento Mensal")

        # Entrada de dados
        renda = st.number_input("Renda Mensal:", value=0.0, step=100.0)
        mercado = st.number_input("Mercado:", value=0.0, step=50.0)
        eletronicos = st.number_input("Eletrônicos:", value=0.0, step=50.0)
        educacao = st.number_input("Educação:", value=0.0, step=50.0)
        transporte = st.number_input("Transporte:", value=0.0, step=50.0)
        superfulos = st.number_input("Supérfluos:", value=0.0, step=50.0)
        investimento = st.number_input("Investimento:", value=0.0, step=50.0)

        despesas = {
            'Mercado': mercado,
            'Eletrônicos': eletronicos,
            'Educação': educacao,
            'Transporte': transporte,
            'Supérfluos': superfulos,
            'Investimento': investimento
        }

        if st.button("Salvar Orçamento"):
            saldo = calcular_saldo(renda, despesas)
            data = datetime.now().strftime("%m/%Y")  # Formato Mês/Ano
            novo_orcamento = {
                'data': data,
                'renda': renda,
                'despesas': despesas,
                'saldo': saldo
            }
            orcamentos.append(novo_orcamento)
            salvar_dados(orcamentos)
            st.success("Orçamento salvo com sucesso!")

        # Mostrar saldo
        saldo = calcular_saldo(renda, despesas)
        st.subheader(f"Saldo Mensal: R$ {saldo:.2f}")

        # Gráfico de gastos
        if st.button("Mostrar Gráfico de Gastos"):
            fig, ax = plt.subplots()
            barras = ax.bar(despesas.keys(), despesas.values(), color='#a51c30')
            ax.set_xlabel('Categorias', color='#FFFFFF')
            ax.set_ylabel('Valor (R$)', color='#FFFFFF')
            ax.set_title('Gastos por Categoria', color='#FFFFFF')
            plt.xticks(rotation=45, color='#FFFFFF')
            plt.yticks(color='#FFFFFF')

            # Adicionar rótulos de dados nas barras
            for barra in barras:
                altura = barra.get_height()
                ax.annotate(f'{altura:.2f}',
                            xy=(barra.get_x() + barra.get_width() / 2, altura),
                            xytext=(0, 5),  # Ajustar deslocamento vertical
                            textcoords="offset points",
                            ha='center', va='bottom', color='#FFFFFF')

            # Definir cor de fundo e remover bordas
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            # Remover eixo Y numérico
            ax.get_yaxis().set_visible(False)

            st.pyplot(fig)

    elif opcao == "Análise e Metas":
        st.header("Análise e Metas")

        if not orcamentos:
            st.warning("Nenhum orçamento salvo ainda.")
        else:
            # Tabela de histórico
            dados_tabela = []
            for orcamento in orcamentos:
                dados_tabela.append([
                    orcamento['data'],
                    orcamento['renda'],
                    orcamento['despesas']['Mercado'],
                    orcamento['despesas']['Eletrônicos'],
                    orcamento['despesas']['Educação'],
                    orcamento['despesas']['Transporte'],
                    orcamento['despesas']['Supérfluos'],
                    orcamento['despesas']['Investimento'],
                    orcamento['saldo']
                ])
            df = pd.DataFrame(dados_tabela, columns=[
                'Data', 'Renda', 'Mercado', 'Eletrônicos', 'Educação', 'Transporte', 'Supérfluos', 'Investimento', 'Saldo'
            ])
            st.dataframe(df)

            # Gráfico de tendências de saldo (barras)
            st.subheader("Tendência de Saldo ao Longo do Tempo")
            datas = [orcamento['data'] for orcamento in orcamentos]
            saldos = [orcamento['saldo'] for orcamento in orcamentos]

            fig1, ax1 = plt.subplots()
            barras = ax1.bar(datas, saldos, color='#a51c30')
            ax1.set_xlabel('Data', color='#FFFFFF')
            ax1.set_ylabel('Saldo (R$)', color='#FFFFFF')
            ax1.set_title('Tendência de Saldo', color='#FFFFFF')
            plt.xticks(rotation=45, color='#FFFFFF')
            plt.yticks(color='#FFFFFF')

            # Adicionar rótulos de dados nas barras
            for barra in barras:
                altura = barra.get_height()
                ax1.annotate(f'{altura:.2f}',
                             xy=(barra.get_x() + barra.get_width() / 2, altura),
                             xytext=(0, 5),  # Ajustar deslocamento vertical
                             textcoords="offset points",
                             ha='center', va='bottom', color='#FFFFFF')

            # Definir cor de fundo e remover bordas
            fig1.patch.set_facecolor('#0E1117')
            ax1.set_facecolor('#0E1117')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
            ax1.spines['left'].set_visible(False)

            # Remover eixo Y numérico
            ax1.get_yaxis().set_visible(False)

            st.pyplot(fig1)

            # Gráfico de crescimento do investimento (linhas)
            st.subheader("Crescimento do Investimento")
            investimentos_acumulados = []
            acumulado = 0
            for orcamento in orcamentos:
                acumulado += orcamento['despesas']['Investimento']
                investimentos_acumulados.append(acumulado)

            fig2, ax2 = plt.subplots()
            linhas = ax2.plot(datas, investimentos_acumulados, marker='o', color='#a51c30')
            ax2.set_xlabel('Data', color='#FFFFFF')
            ax2.set_ylabel('Investimento Acumulado (R$)', color='#FFFFFF')
            ax2.set_title('Crescimento do Investimento', color='#FFFFFF')
            plt.xticks(rotation=45, color='#FFFFFF')
            plt.yticks(color='#FFFFFF')

            # Adicionar rótulos de dados nas linhas
            for x, y in zip(datas, investimentos_acumulados):
                ax2.annotate(f'{y:.2f}',
                             xy=(x, y),
                             xytext=(0, 5),  # Ajustar deslocamento vertical
                             textcoords="offset points",
                             ha='center', va='bottom', color='#FFFFFF')

            # Definir cor de fundo e remover bordas
            fig2.patch.set_facecolor('#0E1117')
            ax2.set_facecolor('#0E1117')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_visible(False)
            ax2.spines['left'].set_visible(False)

            # Remover eixo Y numérico
            ax2.get_yaxis().set_visible(False)

            st.pyplot(fig2)

            # Meta de Investimento
            st.subheader("Meta de Investimento")
            meta_investimento = st.number_input("Defina sua meta de investimento total (R$):", value=0.0, step=1000.0, key='meta_investimento')

            if meta_investimento > 0:
                investimentos_acumulados_total = sum(orcamento['despesas']['Investimento'] for orcamento in orcamentos)
                progresso_investimento = (investimentos_acumulados_total / meta_investimento) * 100
                st.subheader(f"Progresso em relação à Meta de Investimento: {progresso_investimento:.2f}%")
                st.progress(progresso_investimento / 100)

    elif opcao == "Gerenciar Orçamentos":
        st.header("Gerenciar Orçamentos")

        if not orcamentos:
            st.warning("Nenhum orçamento salvo ainda.")
        else:
            # Filtro por período
            st.subheader("Filtrar Orçamentos")
            periodo = st.selectbox("Selecione o período:", ["Todos"] + sorted(list(set(orcamento['data'] for orcamento in orcamentos))))

            # Aplicar filtro
            orcamentos_filtrados = orcamentos
            if periodo != "Todos":
                orcamentos_filtrados = [orcamento for orcamento in orcamentos_filtrados if orcamento['data'] == periodo]

            # Listar orçamentos filtrados
            st.subheader("Orçamentos Filtrados")
            for i, orcamento in enumerate(orcamentos_filtrados):
                with st.expander(f"Orçamento {i + 1} - {orcamento['data']}"):
                    st.write(f"**Renda:** R$ {orcamento['renda']:.2f}")
                    st.write(f"**Saldo:** R$ {orcamento['saldo']:.2f}")
                    st.write("**Despesas:**")
                    for cat, valor in orcamento['despesas'].items():
                        st.write(f"- {cat}: R$ {valor:.2f}")

                    # Botão para editar
                    if st.button(f"Editar Orçamento {i + 1}"):
                        st.session_state['editar_index'] = i

                    # Botão para excluir
                    if st.button(f"Excluir Orçamento {i + 1}"):
                        orcamentos.pop(i)
                        salvar_dados(orcamentos)
                        st.success(f"Orçamento {i + 1} excluído com sucesso!")
                        st.experimental_rerun()

            # Editar orçamento selecionado
            if 'editar_index' in st.session_state:
                st.subheader("Editar Orçamento")
                index = st.session_state['editar_index']
                orcamento = orcamentos[index]

                renda = st.number_input("Renda Mensal:", value=orcamento['renda'], step=100.0)
                mercado = st.number_input("Mercado:", value=orcamento['despesas']['Mercado'], step=50.0)
                eletronicos = st.number_input("Eletrônicos:", value=orcamento['despesas']['Eletrônicos'], step=50.0)
                educacao = st.number_input("Educação:", value=orcamento['despesas']['Educação'], step=50.0)
                transporte = st.number_input("Transporte:", value=orcamento['despesas']['Transporte'], step=50.0)
                superfulos = st.number_input("Supérfluos:", value=orcamento['despesas']['Supérfluos'], step=50.0)
                investimento = st.number_input("Investimento:", value=orcamento['despesas']['Investimento'], step=50.0)

                despesas = {
                    'Mercado': mercado,
                    'Eletrônicos': eletronicos,
                    'Educação': educacao,
                    'Transporte': transporte,
                    'Supérfluos': superfulos,
                    'Investimento': investimento
                }

                if st.button("Salvar Edição"):
                    saldo = calcular_saldo(renda, despesas)
                    orcamentos[index] = {
                        'data': orcamento['data'],
                        'renda': renda,
                        'despesas': despesas,
                        'saldo': saldo
                    }
                    salvar_dados(orcamentos)
                    st.success("Orçamento editado com sucesso!")
                    del st.session_state['editar_index']
                    st.experimental_rerun()

if __name__ == "__main__":
    main()