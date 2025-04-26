import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_excel('dados_vendas_naturalvida.xlsx', decimal=',')
df['Data da Venda'] = pd.to_datetime(df['Data da Venda'])
df=df.sort_values(df['Data da Venda'])


