import streamlit as st
import pandas as pd

# Configuração da página do Streamlit
st.set_page_config(
    page_title='Acompanhamento de Vendas',
    layout='wide'
)

# Cabeçalho com logo e título
col1, col2 = st.columns([1, 12])
with col1:
    st.image('logo.jpg', width=100)
with col2:
    st.title('Acompanhamento de Vendas - Botucaraí Alimentos')

st.markdown("Faça o upload do arquivo no campo lateral")

# DataFrame vazio inicialmente
df = pd.DataFrame()

# Sidebar com upload de arquivo
with st.sidebar:
    arq = st.file_uploader("Upload de arquivo", type=['xlsx', 'csv'])

    if arq is not None:
        if not arq.name.endswith('.xlsx'):
            df = pd.read_csv(arq)
        else:
            df = pd.read_excel(arq)

        st.title('Tabela:')
        st.dataframe(df)

# Processamento dos dados após upload
if arq is not None:
    df = pd.read_excel(arq)

    # Define a ordem correta dos meses do ano
    ordem_meses = ['Janeiro', 'Fevereiro', 'Março']

    # Filtra apenas os meses desejados
    df = df[df['Mês'].isin(ordem_meses)]

    # Converte a coluna 'Mês' para categórica ordenada
    df['Mês'] = pd.Categorical(df['Mês'], categories=ordem_meses, ordered=True)

    # Filtros disponíveis com base nos dados
    lista_vend = df['Vendedor'].unique().tolist()
    lista_mes = ordem_meses  # usa sempre a mesma ordem
    lista_empresa = df['Empresa'].unique().tolist()

    # Filtros de seleção do usuário
    vend_selecionado = st.multiselect('Selecione o vendedor', lista_vend)
    mes_selecionado = st.multiselect('Selecione o mês', lista_mes)
    empresa_selecionada = st.selectbox('Selecione a empresa', lista_empresa)

    # Aplica os filtros
    filtrado = df[
        (df['Vendedor'].isin(vend_selecionado)) &
        (df['Mês'].isin(mes_selecionado)) &
        (df['Empresa'] == empresa_selecionada)
    ]

    # Reordena os meses filtrados
    filtrado['Mês'] = pd.Categorical(filtrado['Mês'], categories=ordem_meses, ordered=True)
    filtrado = filtrado.sort_values('Mês')

    # Divide a tela em duas colunas para gráficos
    col1, col2 = st.columns([1, 3])

    # Gráfico de barras por vendedor
    with col1:
        st.subheader('Vendas por Empresa')
        if not filtrado.empty:
            st.bar_chart(filtrado.set_index('Vendedor')['Faturamento'])
        else:
            st.info("Nenhum dado disponível com os filtros aplicados.")

    # Gráfico de linha por mês e vendedor
    with col2:
        st.subheader('Faturamento por Vendedor ao Longo dos Meses')
        if not filtrado.empty:
            tabela_linhas = filtrado.pivot_table(
                index='Mês',
                columns='Vendedor',
                values='Faturamento',
                aggfunc='sum'
            ).reindex(mes_selecionado)  # garante que só apareçam os meses filtrados e na ordem correta

            st.line_chart(tabela_linhas)
        else:
            st.info("Nenhum dado disponível com os filtros aplicados.")

    # Gráfico de faturamento mensal geral
    st.title('Faturamento Mensal (Geral)')
    df_geral = df[
        (df['Vendedor'].isin(vend_selecionado)) &
        (df['Mês'].isin(mes_selecionado)) &
        (df['Empresa'] == empresa_selecionada)
    ]
    if not df_geral.empty:
        df_geral = df_geral.sort_values('Mês')
        st.bar_chart(df_geral.groupby('Mês')['Faturamento'].sum())
    else:
        st.info("Nenhum dado disponível com os filtros aplicados.")
