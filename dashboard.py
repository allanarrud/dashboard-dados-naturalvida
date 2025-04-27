import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(layout='wide')

df = pd.read_excel('dados_vendas_naturalvida.xlsx', decimal=',')
df['Data da Venda'] = pd.to_datetime(df['Data da Venda'])
df = df.sort_values(by='Data da Venda')


df['month'] = df['Data da Venda'].apply(lambda x: str(x.year) + '-' + str(x.month))
month = st.sidebar.selectbox('Mês', df['month'].unique())

df_filtered = df[df['month'] == month]


data_hoje = df_filtered['Data da Venda'].max()
df_filtered['Dias Sem Venda'] = (data_hoje - df_filtered['Data da Venda']).dt.days

produtos_parados = df_filtered[df_filtered['Dias Sem Venda'] > 60]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x='Data da Venda', y='Total Venda (R$)', color='Preço Unitário (R$)', title='Faturamento por dia')
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x='Data da Venda', y='Produto', color='Margem de Lucro (%)', title='Faturamento por tipo de produto',
                  orientation='h')
col2.plotly_chart(fig_prod, use_container_width=True)

fig_produtos_parados = px.bar(
    produtos_parados,
    x='Produto', 
    y='Dias Sem Venda',
    color='Dias Sem Venda',
    color_continuous_scale='reds',
    title='Produtos Parados há mais de 60 dias'
)
col3.plotly_chart(fig_produtos_parados, use_container_width=True)

vendas_mensais = df.groupby('month').agg({'Quantidade Vendida' : 'sum'}).reset_index()

fig_vendas_sazonais = px.pie(vendas_mensais, names='month', values='Quantidade Vendida', title='Participação nas Vendas por Mês', color_discrete_sequence=px.colors.sequential.RdBu)

st.plotly_chart(fig_vendas_sazonais, use_container_width=True)

