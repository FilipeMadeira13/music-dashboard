import streamlit as st
import plotly.express as px

from last_fm import enrich_albums, fetch_lastfm, normalize_albums


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
quantity = st.text_input("Número de álbuns", 10)

if artist:
    df = load_data(artist, quantity)

    df = df.sort_values(by="rank").reset_index(drop=True)

    st.dataframe(df)
