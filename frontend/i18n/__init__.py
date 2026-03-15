from __future__ import annotations

from importlib import import_module

SUPPORTED = ["pt", "en"]
DEFAULT = "pt"


def get_strings(lang: str | None) -> dict[str, str]:
    if lang not in SUPPORTED:
        lang = DEFAULT
    module = import_module(f"frontend.i18n.{lang}")
    return module.STRINGS  # type: ignore[attr-defined]


def t(strings: dict, key: str, **kwargs) -> str:
    """Return translated string; falls back to the key itself."""
    text = strings.get(key, key)
    return text.format(**kwargs) if kwargs else text
