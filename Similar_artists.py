import pandas as pd
import plotly.express as px
import streamlit as st

from last_fm import fetch_lastfm

## Organização dos dados
data = fetch_lastfm("artist.getsimilar", artist="Iron Maiden", limit=250)
artists = data["similarartists"]["artist"]

df = pd.json_normalize(artists)
df = df[["name", "match"]]

## Dashboard
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")


media_match = df["match"].astype(float).mean()

### Dashboard/Métricas
col1, col2 = st.columns(2)

with col1:
    st.metric("Similaridade média do Artista", f"{media_match:.2f}")

with col2:
    st.metric("Número de Artistas similares", df.shape[0])

### Dashboard/Tabela
st.dataframe(df)
