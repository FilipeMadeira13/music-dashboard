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


@st.cache_data(show_spinner=False)
def get_album_info(artist: str, album: str) -> Dict[str, Any]:
    return fetch_lastfm(
        "album.getinfo",
        artist=artist,
        album=album,
    )


# ------------------------
# NORMALIZATION
# ------------------------
def normalize_albums(albums: List[Dict[str, Any]]) -> pd.DataFrame:
    data = [
        {
            "album_name": a.get("name"),
            "artist_name": a.get("artist", {}).get("name"),
            "playcount": parse_int(a.get("playcount"), 0),
            "rank": parse_int(a.get("@attr", {}).get("rank"), 0),
        }
        for a in albums
    ]

    return pd.DataFrame(data)


def normalize_tracks(tracks: List[Dict[str, Any]]) -> pd.DataFrame:
    data = [
        {
            "track_name": t.get("name"),
            "artist_name": t.get("artist", {}).get("name"),
            "playcount": parse_int(t.get("playcount")),
            "listeners": parse_int(t.get("listeners")),
            "rank": parse_int(t.get("@attr", {}).get("rank")),
        }
        for t in tracks
    ]

    return pd.DataFrame(data)


# ------------------------
# ENRICHMENT
# ------------------------


def _resolve_track_count(tracks: Any) -> int:
    if isinstance(tracks, list):
        return len(tracks)
    if isinstance(tracks, dict):
        return 1
    return 0


@st.cache_data(show_spinner=True)
def enrich_albums(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if df.empty:
        return pd.DataFrame(
            columns=[
                "album_name",
                "artist_name",
                "playcount",
                "rank",
                "listeners",
                "track_count",
                "plays_per_track",
                "plays_per_listener",
            ]
        )

    records = []

    for row in df.itertuples(index=False):
        album_name = getattr(row, "album_name", None)
        artist_name = getattr(row, "artist_name", None)
        playcount = parse_int(getattr(row, "playcount", None), 0)
        rank = parse_int(getattr(row, "rank", None), 0)

        if not album_name or not artist_name:
            records.append(
                {
                    "album_name": album_name,
                    "artist_name": artist_name,
                    "playcount": playcount,
                    "rank": rank,
                    "listeners": None,
                    "track_count": 0,
                    "plays_per_track": None,
                    "plays_per_listener": None,
                }
            )
            continue

        response = get_album_info(str(artist_name), str(album_name))
        album = response.get("album", {}) if isinstance(response, dict) else {}

        listeners = parse_int(album.get("listeners"))
        tracks = album.get("tracks", {}).get("track", [])
        track_count = _resolve_track_count(tracks)

        records.append(
            {
                "album_name": album_name,
                "artist_name": artist_name,
                "playcount": playcount,
                "rank": rank,
                "listeners": listeners,
                "track_count": track_count,
                "plays_per_track": _safe_div(playcount, track_count),
                "plays_per_listener": _safe_div(playcount, listeners),
            }
        )

    return pd.DataFrame(records)
