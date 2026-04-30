from typing import Optional, Union, Any


def parse_int(
    value: Union[str, int, float, None], default: Optional[int] = None
) -> Optional[int]:
    if value is None:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def dataframe_to_csv_bytes(df: Any) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
