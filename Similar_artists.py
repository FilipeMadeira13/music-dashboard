import pandas as pd
import plotly.express as px
import streamlit as st

from last_fm import fetch_lastfm


## Organização dos dados
@st.cache_data(show_spinner=True)
def load_data(artist, quantity):
    data = fetch_lastfm("artist.getsimilar", artist=artist, limit=quantity)
    artists = data["similarartists"]["artist"]

    df = pd.json_normalize(artists)
    df = df[["name", "match"]]
    return df


## Dashboard
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

artist = st.text_input("Digite o artista", "Metallica")
quantity = st.text_input("Número de artistas", 10)

if artist:
    df = load_data(artist, quantity)
    df.columns = ["Artista", "Match"]

    ### Gráficos
    fig_match = px.line(
        df,
        x="Artista",
        y="Match",
        range_y=(0, df.Match.max()),
        title="Similaridade com o artista",
    )

    ### Dashboard/Métricas

    media_match = df["Match"].astype(float).mean()
    st.metric("Similaridade média do Artista", f"{media_match:.2f}")

    ### Dashboard/Tabela
    st.dataframe(df)
    st.plotly_chart(fig_match)
