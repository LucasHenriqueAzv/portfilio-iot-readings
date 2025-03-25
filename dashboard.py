import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# conexao com o db
postgres_password = os.getenv("POSTGRES_PASSWORD")
connection_string = f"postgresql://postgres:{postgres_password}@localhost:5432/postgres"
engine = create_engine(connection_string)

# carregar dados de uma view
def load_data(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# dash

st.title("Dashboard de Temperaturas IoT")

# grafico 1: media de temperatura por local
st.header("Média de Temperatura por Local (Interno/Externo)")
df_avg_temp = load_data("avg_temp_por_local")
fig1 = px.bar(
    df_avg_temp,
    x="sensor_location",
    y="avg_temp",
    title="Média de Temperatura por Local",
    labels={"sensor_location": "Local do Sensor", "avg_temp": "Temperatura Média"}
)
st.plotly_chart(fig1)

# grafico 2: vontagem de leituras por hora do dia
st.header("Leituras por Hora do Dia")
df_leituras_hora = load_data("leituras_por_hora")
fig2 = px.line(
    df_leituras_hora,
    x="hora",
    y="contagem",
    title="Contagem de Leituras por Hora",
    markers=True,
    labels={"hora": "Hora do Dia", "contagem": "Número de Leituras"}
)
st.plotly_chart(fig2)

# grafico 3: temperaturas max e min por dia
st.header("Temperaturas Máximas e Mínimas por Dia")
df_temp_max_min = load_data("temp_max_min_por_dia")
fig3 = px.line(
    df_temp_max_min,
    x="data",
    y=["temp_max", "temp_min"],
    title="Temperaturas Máximas e Mínimas por Dia",
    markers=True,
    labels={"data": "Data", "value": "Temperatura", "variable": "Métrica"}
)

st.plotly_chart(fig3)
