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


# ------------------------
# UI
# ------------------------
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

artist = st.text_input("Digite o artista", "Metallica")
quantity = st.number_input("Número de artistas", min_value=2, max_value=250, value=10)

if artist:
    df = load_data(artist, quantity)

    if df.empty:
        st.warning("Nenhum artista encontrado.")
        st.stop()

    # ------------------------
    # METRICS
    # ------------------------
    media_match = df["Match"].mean()
    st.metric("Similaridade média do Artista", f"{media_match:.2f}")

    # ------------------------
    # CHART
    # ------------------------
    fig_match = px.line(
        df,
        x="Artista",
        y="Match",
        title="Similaridade com o artista",
    )
    st.plotly_chart(fig_match, use_container_width=True)

    # ------------------------
    # TABLE
    # ------------------------
    with st.expander("Colunas"):
        selected_columns = st.multiselect(
            "Selecione as colunas",
            options=df.columns.tolist(),
            default=df.columns.tolist(),
        )
    st.dataframe(df[selected_columns], use_container_width=True)

    # ------------------------
    # DOWNLOAD
    # ------------------------
    st.markdown("### Exportar dados")

    col1, col2 = st.columns(2)

    with col1:
        file_name = st.text_input(
            "Nome do arquivo",
            value="similar_artists",
            label_visibility="collapsed",
        )

    with col2:
        st.download_button(
            "Baixar CSV",
            data=dataframe_to_csv_bytes(df[selected_columns]),
            file_name=f"{file_name}.csv",
            mime="text/csv",
            on_click=show_success_message,
        )
