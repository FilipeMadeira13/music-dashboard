import os

from dotenv import load_dotenv


def load_environment() -> None:
    load_dotenv()


def get_api_key() -> str:
    api_key = os.getenv("API_KEY")

    if not api_key:
        try:
            import streamlit as st

            api_key = st.secrets.get("API_KEY")
        except Exception:
            pass

    if not api_key:
        raise ValueError("API_KEY não encontrada")

    return api_key


BASE_URL: str = "http://ws.audioscrobbler.com/2.0/"
