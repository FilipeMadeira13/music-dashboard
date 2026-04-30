from typing import Any, Optional, Union


def parse_int(
    value: Union[str, int, float, None], default: Optional[int] = None
) -> Optional[int]:
    if value is None:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_div(
    numerator: int | float | None,
    denominator: int | float | None,
) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def dataframe_to_csv_bytes(df: Any) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
