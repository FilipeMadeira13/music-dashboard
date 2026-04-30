import requests
import pandas as pd
import streamlit as st
from typing import Any, Dict, List

from config import BASE_URL, get_api_key, load_environment
from utils.utils import parse_int, _safe_div

load_environment()
API_KEY = get_api_key()


# ------------------------
# HTTP CORE
# ------------------------
@st.cache_data(show_spinner=False)
def fetch_lastfm(method: str, **kwargs) -> Dict[str, Any]:
    if not isinstance(method, str) or not method:
        raise ValueError("method must be a non-empty string")

    params = {
        "method": method,
        "api_key": API_KEY,
        "format": "json",
        **kwargs,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}


@st.cache_data
def get_album_info(artist, album):
    params = {
        "method": "album.getinfo",
        "artist": artist,
        "album": album,
        "api_key": API_KEY,
        "format": "json",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {}

    return response.json()


# ------------------------
# Normalização
# ------------------------
def normalize_albums(albums):
    normalized = []

    for a in albums:
        normalized.append(
            {
                "album_name": a.get("name"),
                "artist_name": a.get("artist", {}).get("name"),
                "playcount": int(a.get("playcount", 0)),
                "rank": int(a.get("@attr", {}).get("rank", 0)),
            }
        )

    return pd.DataFrame(normalized)


def normalize_tracks(tracks):
    data = []

    for t in tracks:
        track_data = {
            "track_name": t.get("name"),
            "artist_name": t.get("artist", {}).get("name"),
            "playcount": int(t.get("playcount", 0)),
            "listeners": int(t.get("listeners", 0)),
            "rank": int(t.get("@attr", {}).get("rank", 0)),
        }

        data.append(track_data)

    return pd.DataFrame(data)


@st.cache_data(show_spinner=True)
def enrich_albums(df):
    df = df.copy()
    enriched = []

    for row in df.itertuples(index=False):
        data = get_album_info(row.artist_name, row.album_name)
        album = data.get("album", {})

        listeners = parse_int(album.get("listeners"))
        tracks = album.get("tracks", {}).get("track", [])
        track_count = len(tracks) if isinstance(tracks, list) else 1
        release_date = str(album.get("releasedate", "")).strip() or None

        enriched.append(
            {
                "album_name": row.album_name,
                "artist_name": row.artist_name,
                "playcount": row.playcount,
                "rank": row.rank,
                "listeners": listeners,
                "track_count": track_count,
                "plays_per_track": row.playcount / track_count if track_count else None,
                "plays_per_listener": row.playcount / listeners if listeners else None,
            }
        )

    return pd.DataFrame(enriched)
