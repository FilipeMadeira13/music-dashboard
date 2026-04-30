import pandas as pd
import streamlit as st

from api.lastfm_client import fetch_lastfm, normalize_tracks
from ui.notifications import show_success_message
from utils.utils import dataframe_to_csv_bytes

st.set_page_config(page_icon="🎵", page_title="Dashboard Musical")


## Organização dos dados
@st.cache_data(show_spinner=True)
def load_data(artist, quantity):
    data = fetch_lastfm("artist.gettoptracks", artist=artist, limit=quantity)
    tracks = data["toptracks"]["track"]

    df = normalize_tracks(tracks)
    df["plays_per_listener"] = df["playcount"] / df["listeners"].replace(0, 1)
    return df


## Dashboard
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

artist = st.text_input("Digite o artista", "Metallica")
quantity = st.number_input("Número de faixas", 2, 500, 50)

### Dashboard/Métricas
col1, col2 = st.columns(2)

if artist:
    df = load_data(artist, quantity)
    with col1:
        st.metric("Playcount Total", df["playcount"].sum(), format="compact")
    with col2:
        total_plays = df["playcount"].sum()
        total_listeners = df["listeners"].sum()
        global_ratio = total_plays / total_listeners
        # ~1.0 → pessoas ouvem só 1 vez (baixo engajamento)
        # 2–3 → engajamento médio
        # 4+ → fãs fortes (muito replay)
        st.metric(label="Plays por Listener", value=f"{global_ratio:.2f}")

    ### Dashboard/Tabela
    with st.expander("Colunas"):
        colunas = st.multiselect(
            "Selecione as colunas", list(df.columns), list(df.columns)
        )
    st.title("Top Tracks", text_alignment="center")

    st.dataframe(df[colunas])
    st.markdown("Escreva um nome para o arquivo")
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        nome_arquivo = st.text_input(
            "Nome do arquivo",
            label_visibility="collapsed",
            value="tracks",
            key="tracks_input",
        )
        nome_arquivo += ".csv"
    with coluna2:
        st.download_button(
            "Fazer o download da tabela em CSV",
            data=dataframe_to_csv_bytes(df),
            file_name=nome_arquivo,
            mime="text/csv",
            on_click=show_success_message,
        )
