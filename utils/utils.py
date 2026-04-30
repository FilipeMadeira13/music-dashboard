import time
from typing import Optional, Union
import streamlit as st


def parse_int(
    value: Union[str, int, float, None], default: Optional[int] = None
) -> Optional[int]:
    if value is None:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def mensagem_sucesso():
    sucesso = st.success("Arquivo baixado com sucesso!", icon="✅")
    time.sleep(5)
    sucesso.empty()
