import pandas as pd
import streamlit as st

from last_fm import fetch_lastfm, normalize_tracks


## Organização dos dados
data = fetch_lastfm("artist.gettoptracks", artist="Bob Dylan", limit=100)
tracks = data["toptracks"]["track"]

df = normalize_tracks(tracks)
df["plays_per_listener"] = df["playcount"] / df["listeners"].replace(0, 1)

## Dashboard
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")

### Dashboard/Métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Número de Faixas", df.shape[0])
with col2:
    st.metric("Playcount Total", df["playcount"].sum(), format="compact")

with col3:
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
