import pandas as pd
import streamlit as st

from last_fm import fetch_lastfm, normalize_tracks


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
quantity = st.text_input("Número de álbuns", 10)

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
    st.title("Top Tracks", text_alignment="center")

    st.dataframe(df)
