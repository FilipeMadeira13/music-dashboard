import pandas as pd
import streamlit as st

from last_fm import enrich_albums, fetch_lastfm, get_album_info, normalize_albums

## Organização dos dados
data = fetch_lastfm("artist.gettopalbums", artist="Running Wild", limit=20)


albums = data["topalbums"]["album"]

df = normalize_albums(albums)
df = enrich_albums(df)

df = df.sort_values(by="plays_per_track", ascending=False).reset_index(drop=True)

## Dashboard
st.title("Dashboard Musical :red[last.fm]", text_alignment="center")
st.title("Top Albums", text_alignment="center")

st.metric("Número de Álbuns", df.shape[0])


### Dashboard/Tabela
st.dataframe(df)
