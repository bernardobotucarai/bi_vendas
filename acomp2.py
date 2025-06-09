import streamlit as st
import pandas as pd
from PIL import Image

def barras(df_pivot):
    st.bar_chart(df_pivot)

def linhas(df_pivot):
    st.line_chart(df_pivot)

imagem = Image.open('logo.jpg') # lendo o logo da empresa

st.set_page_config(
    page_title = 'BI - Acompanhamento de Vendas',
    page_icon = imagem, # atribuindo o logo da empresa como ícone da página
    layout = 'wide'
    )

col1, col2 = st.columns([1,10])
with col1:
    st.image(imagem, width=90)

with col2:
    st.title('BI - Acompanhamento de Vendas')
    st.markdown('Carregue o arquivo no campo lateral')

df = pd.DataFrame()

with st.sidebar:
    arq = st.file_uploader('Carregue um arquivo no campo abaixo', type=['csv', 'xlsx'])

    if arq is not None:
        if arq.name.endswith('.xlsx'):
            df = pd.read_excel(arq)
        else:
            df = pd.read_csv(arq)
        st.dataframe(df)

if arq is not None:

    vendedores = df['Vendedor'].unique().tolist()
    meses = df['Mês'].unique().tolist()
    empresa = df['Empresa'].unique().tolist()

    vend_selecionado = st.multiselect('Selecione o vendedor',vendedores, placeholder='Vendedor')
    mes_selecionado = st.multiselect('Selecione o mês',meses,placeholder='Mês')
    empresa_selecionada = st.multiselect('Selecione a empresa',empresa,placeholder='Empresa')

    df_filtrado = df[
        df['Vendedor'].isin(vend_selecionado) &
        df['Mês'].isin(mes_selecionado) &
        df['Empresa'].isin(empresa_selecionada)
    ]

    col4, col5 = st.columns([1,2])

    if not df_filtrado.empty:
        with col4:
            df_agrupado = df_filtrado.groupby(['Mês', 'Empresa', 'Vendedor'])['Faturamento'].sum().reset_index()
            df_agrupado['Empresa_Vendedor'] = df_agrupado['Empresa'] + ' - ' + df_agrupado['Vendedor']
            df_pivot = df_agrupado.pivot(index='Mês', columns='Empresa_Vendedor', values='Faturamento')  # define o eixo X
            st.subheader('**Gráfico de barras**')
            st.markdown(f"""
            **Empresa selecionada:** {", ".join(empresa_selecionada)}  
            **Vendedor selecionado:** {", ".join(vend_selecionado)}
            """)
            barras(df_pivot)

        with col5:
            df_agrupado = df_filtrado.groupby(['Mês', 'Empresa', 'Vendedor'])['Faturamento'].sum().reset_index()
            df_agrupado['Empresa_Vendedor'] = df_agrupado['Empresa'] + ' - ' + df_agrupado['Vendedor']
            df_pivot = df_agrupado.pivot(index='Mês', columns='Empresa_Vendedor',
                                         values='Faturamento')  # define o eixo X
            st.subheader('**Gráfico de linhas**')
            st.markdown(f"""
            **Empresa selecionada:** {", ".join(empresa_selecionada)}  
            **Vendedor selecionado:** {", ".join(vend_selecionado)}
            """)
            linhas(df_pivot)

        st.subheader('**Faturamento mensal por empresa**')
        st.markdown(f'''**Empresa selecionada:** {", ".join(empresa_selecionada)}''')

        df_mes = df_agrupado.pivot(index='Mês', columns='Empresa_Vendedor', values='Faturamento')
        df_empresa_total = df_filtrado.groupby('Empresa')['Faturamento'].sum().reset_index()
        df_empresa_total = df_empresa_total.set_index('Empresa')
        barras(df_empresa_total)

    else:
        st.info('Nenhum filtro selecionado')