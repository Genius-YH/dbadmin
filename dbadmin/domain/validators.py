import re

IDENT_RE = re.compile(r"^[A-Za-z0-9_]+$")
HOST_RE = re.compile(r"^[A-Za-z0-9_%.:-]+$")


def is_valid_ident(value: str) -> bool:
    return bool(value and IDENT_RE.fullmatch(value))


def is_valid_host(value: str) -> bool:
    return bool(value and HOST_RE.fullmatch(value))


def quote_ident(value: str) -> str:
    if not is_valid_ident(value):
        raise ValueError(f"Invalid identifier: {value}")
    return f"`{value}`"


def quote_string(value: str) -> str:
    return "'" + (value or "").replace("\\", "\\\\").replace("'", "\\'") + "'"
