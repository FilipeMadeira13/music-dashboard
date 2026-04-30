import streamlit as st
import plotly.express as px

from api.lastfm_client import (
    enrich_albums,
    fetch_lastfm,
    normalize_albums,
)
from utils.utils import converte_csv, mensagem_sucesso

st.set_page_config(page_icon="🎵", page_title="Dashboard Musical")


# ------------------------
# Carregamento de dados
# ------------------------
@st.cache_data(show_spinner=True)
def load_data(artist, quantity):
    artist = artist.strip()

    data = fetch_lastfm("artist.gettopalbums", artist=artist, limit=quantity)
    albums = data["topalbums"]["album"]

    df = normalize_albums(albums)
    df = enrich_albums(df)

    return df


# ------------------------
# Dashboard
# ------------------------
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

artist = st.text_input("Digite o artista", "Metallica")
quantity = st.number_input("Número de álbuns", 2, 50, 10)

if artist:
    df = load_data(artist, quantity)

    df = df.sort_values(by="rank").reset_index(drop=True)

    with st.expander("Colunas"):
        colunas = st.multiselect(
            "Selecione as colunas", list(df.columns), list(df.columns)
        )
    st.dataframe(df[colunas])
    st.markdown("Escreva um nome para o arquivo")
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        nome_arquivo = st.text_input("", label_visibility="collapsed", value="albums")
        nome_arquivo += ".csv"
    with coluna2:
        st.download_button(
            "Fazer o download da tabela em CSV",
            data=converte_csv(df),
            file_name=nome_arquivo,
            mime="text/csv",
            on_click=mensagem_sucesso,
        )
