import pandas as pd
import plotly.express as px
import streamlit as st

from api.lastfm_client import fetch_lastfm
from ui.notifications import show_success_message
from utils.utils import dataframe_to_csv_bytes

st.set_page_config(page_icon="🎵", page_title="Dashboard Musical")


# ------------------------
# DATA
# ------------------------
@st.cache_data(show_spinner=True)
def load_data(artist: str, quantity: int) -> pd.DataFrame:
    data = fetch_lastfm("artist.getsimilar", artist=artist, limit=quantity)
    artists = data.get("similarartists", {}).get("artist", [])

    df = pd.json_normalize(artists)
    df = df[["name", "match"]].rename(
        columns={
            "name": "Artista",
            "match": "Match",
        }
    )
    df["Match"] = pd.to_numeric(df["Match"], errors="coerce").fillna(0)
    return df


## Dashboard
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

artist = st.text_input("Digite o artista", "Metallica")
quantity = st.number_input("Número de artistas", 2, 250, 10)

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
    with st.expander("Colunas"):
        colunas = st.multiselect(
            "Selecione as colunas", list(df.columns), list(df.columns)
        )
    st.dataframe(df[colunas])
    st.plotly_chart(fig_match)
    st.markdown("Escreva um nome para o arquivo")
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        nome_arquivo = st.text_input(
            "Nome do arquivo",
            label_visibility="collapsed",
            value="similar_artists",
            key="artist_input",
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
