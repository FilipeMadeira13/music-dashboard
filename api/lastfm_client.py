import requests
import pandas as pd
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    params.update(dict(sorted(kwargs.items())))

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.warning(f"Last.fm request failed: {e}")
        return {}


@st.cache_data(ttl=3600)
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
    if not tracks:
        return 0
    return len(tracks) if isinstance(tracks, list) else 1


def _build_album_record(
    album_name: str | None,
    artist_name: str | None,
    playcount: int | None,
    rank: int | None,
) -> Dict[str, Any]:
    base = {
        "album_name": album_name,
        "artist_name": artist_name,
        "playcount": parse_int(playcount, 0),
        "rank": parse_int(rank, 0),
    }

    if not album_name or not artist_name:
        return {
            **base,
            "listeners": None,
            "track_count": 0,
            "plays_per_track": None,
            "plays_per_listener": None,
        }

    response = get_album_info(str(artist_name), str(album_name))
    album = response.get("album", {}) if response else {}
    listeners = parse_int(album.get("listeners"))
    tracks = album.get("tracks", {}).get("track", [])
    track_count = len(tracks) if isinstance(tracks, list) else 1 if tracks else 0

    return {
        **base,
        "listeners": listeners,
        "track_count": track_count,
        "plays_per_track": _safe_div(playcount, track_count),
        "plays_per_listener": _safe_div(playcount, listeners),
    }


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

    records: list[Dict[str, Any] | None] = [None] * len(df)
    max_workers = min(8, len(df))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _build_album_record,
                getattr(row, "album_name", None),
                getattr(row, "artist_name", None),
                parse_int(getattr(row, "playcount", None)) or 0,
                parse_int(getattr(row, "rank", None)) or 0,
            ): idx
            for idx, row in enumerate(df.itertuples(index=False))
        }

        for future in as_completed(futures):
            idx = futures[future]
            records[idx] = future.result()

    return pd.DataFrame(records)
