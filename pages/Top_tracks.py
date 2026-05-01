import pandas as pd
import streamlit as st

from api.lastfm_client import fetch_lastfm, normalize_tracks
from ui.notifications import show_success_message
from utils.utils import dataframe_to_csv_bytes, _safe_div

st.set_page_config(page_icon="🎵", page_title="Dashboard Musical")


# ------------------------
# DATA
# ------------------------
@st.cache_data(show_spinner=True)
def load_data(artist: str, quantity: int) -> pd.DataFrame | None:
    artist = artist.strip()

    if not artist:
        return None

    data = fetch_lastfm("artist.gettoptracks", artist=artist, limit=quantity)

    tracks = data.get("toptracks", {}).get("track", [])

    if not tracks:
        return None

    df = normalize_tracks(tracks)

    if df.empty:
        return None

    df["plays_per_listener"] = [
        _safe_div(p, l) for p, l in zip(df["playcount"], df["listeners"])
    ]
    df = df.drop(columns=["artist_name"], errors="ignore")

    return df


# ------------------------
# UI
# ------------------------
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

artist = st.text_input("Digite o artista", "Metallica")
quantity = st.number_input("Número de faixas", min_value=2, max_value=500, value=50)

col1, col2 = st.columns(2)

if artist:
    df = load_data(artist, quantity)

    if df is None or df.empty:
        st.warning("Nenhuma faixa encontrada.")
        st.stop()

    # ------------------------
    # METRICS
    # ------------------------
    total_plays = df["playcount"].sum()
    total_listeners = df["listeners"].sum()

    with col1:
        st.metric("Playcount Total", total_plays, delta=None)

    with col2:
        global_ratio = _safe_div(total_plays, total_listeners)
        st.metric(
            label="Plays por Listener",
            value=f"{global_ratio:.2f}" if global_ratio else "N/A",
        )

    # ------------------------
    # TABLE
    # ------------------------
    st.title("Top Tracks", text_alignment="center")

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
            value="tracks",
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
