#importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px


dados = pd.read_excel('./Dados_Comerciais.xlsx') #Lendo e criando os data frame

#cabeçalho da pagina
st.set_page_config(
    page_title='Analise de vendas',
    page_icon="📊",
    layout='wide',
)


st.sidebar.header("🔎 Filtros")

Estado = dados['Estado'].unique()
Estados_selecionados = st.sidebar.multiselect('Estados', Estado, default=Estado)

Segmentacao = dados['Segmento'].unique()
Segmentacoes_selecionadas = st.sidebar.multiselect('Segmentações', Segmentacao, default=Segmentacao)

st.markdown(
    """
    <style>
    /* Chip inteiro */
    [data-baseweb="tag"] {
        background-color: #0066cc !important; /* Azul */
        color: white !important;
    }

    /* Texto dentro do chip */
    [data-baseweb="tag"] span {
        color: white !important;
    }

    /* Ícone X dentro do chip */
    [data-baseweb="tag"] svg {
        fill: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


dados_filtrados= dados[
    (dados['Estado'].isin(Estados_selecionados))&
    (dados['Segmento'].isin(Segmentacoes_selecionadas))
    
]
dados_filtrados_e = dados[
    (dados['Estado'].isin(Estados_selecionados))
]
dados_filtrados_s = dados[
    (dados['Segmento'].isin(Segmentacoes_selecionadas))
]

st.title('💻 Dashboard de Análise de Vendas')
st.markdown('Análise de dados fictícios de vendas com fins de aprendizado de modelagem de dados utilizando Phyton e suas bibliotecas: streamlit, pandas e plotly.')

st.subheader("📐 Métricas gerais")

if not dados_filtrados.empty:
    quant_venda = len(dados_filtrados)  
    volume_venda = dados_filtrados['ValorVenda'].sum()
    qtd_estados = dados_filtrados['Estado'].nunique()
else:
    quant_venda, volume_venda, qtd_estados = 0, 0, 0
    
col1, col2, col3 = st.columns(3)


col1.metric('Total de vendas analisadas', f'{quant_venda:,}'.replace(',', '.'))
col2.metric('Volume total de vendas', f"R$ {volume_venda:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.'))
col3.metric('Quantidade de Estados Atuantes', f'{qtd_estados}')

st.markdown('______')

st.subheader('📈 Graficos')

graf_01, graf_02 = st.columns(2)

with graf_01:
    if not dados_filtrados_e.empty:
        qtd_vendedor_estado = dados_filtrados_e.groupby('Estado')['ID-Vendedor'].nunique().sort_values(ascending=True).reset_index()
    
        fig1 = px.bar(
            qtd_vendedor_estado,
            x='ID-Vendedor',
            y='Estado',
            title='🔢 Quantidade de Vendedores por Estado'
        )
    
        fig1.update_traces(
        hovertemplate = 'Quantidade de Vendedores no Estado de %{y}: %{x}'
        )
        fig1.update_layout(
            xaxis_title='Quantidade de Vendedores'
        )
    else:
        st.warning("Não há dados selecionados para a criação do gráfico")
    
    st.plotly_chart(fig1)

with graf_02:
    if not dados_filtrados.empty:
    # Agrupando valor total por segmento
        vendas_por_segmento = dados_filtrados.groupby('Segmento')['ValorVenda'].sum().reset_index()

    # Criando gráfico de pizza com Plotly
        fig2 = px.pie(
            vendas_por_segmento,
            values='ValorVenda',
            names='Segmento',
            title='💰 Valor de Vendas Por Segmento'
        )
   
        fig2.update_traces(
            textposition='inside',
            texttemplate='%{label}<br>%{percent:.2%}',
            hovertemplate='<b>%{label}</b><br>Vendas: R$ %{value:,.2f}<extra></extra>'
        )
        fig2.update_layout(margin=dict(t=40, r=10, b=10, l=10))
  
        st.plotly_chart(fig2)
    else:
        st.warning("Não há dados selecionados para a criação do gráfico")

graf_03, graf_04 = st.columns(2)

with graf_03:
    if not dados_filtrados.empty:
        vendas_por_fabricantes = dados_filtrados.groupby('Fabricante')['ValorVenda'].sum().sort_values(ascending=False).reset_index()
    
        fig3 = px.bar(
            vendas_por_fabricantes,
            x='Fabricante',
            y='ValorVenda',
            text='ValorVenda',
            title='🏷️ Total de Vendas Por Fabricante'
            )
        
    
        fig3.update_layout(
            xaxis_title='Fabricante',
            yaxis_title='Valor Total de Vendas',
        )
    
        fig3.update_traces(
            textposition='outside',
            hovertemplate='Total de Vendas %{x}: R$ %{text:.2f}<extra></extra>'
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Não há dados selecionados para a criação do gráfico")      

with graf_04:
    if not dados_filtrados.empty:
        venda_por_categoria = dados_filtrados.groupby('Categoria')['ValorVenda'].sum().reset_index()
        venda_por_categoria = venda_por_categoria.sort_values('ValorVenda', ascending=False)

    # Criando uma coluna já formatada em R$ com separador brasileiro
        venda_por_categoria['ValorVenda_fmt'] = venda_por_categoria['ValorVenda'].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        fig4 = px.funnel(
            venda_por_categoria,
            x='ValorVenda',
            y='Categoria',
            title='📈 Valor Total de Vendas por Categoria'
        )
    
    # Usando a coluna formatada como texto
        fig4.update_traces(
            text=venda_por_categoria['ValorVenda_fmt'],
            textposition='inside',
            textinfo='text',
            hovertemplate='Total de Vendas %{y}: %{text}<extra></extra>'
        )

        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("Não há dados selecionados para a criação do gráfico")  