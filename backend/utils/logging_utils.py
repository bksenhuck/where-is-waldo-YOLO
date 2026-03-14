"""
Centralised logging configuration for the Where-is-Waldo project.

Usage (in any module)
---------------------
    from backend.utils.logging_utils import get_logger
    log = get_logger(__name__)
    log.info("message")

Usage (in a script entrypoint / main())
----------------------------------------
    from backend.utils.logging_utils import setup_logging
    setup_logging()          # INFO by default
    setup_logging(logging.DEBUG)
"""

from __future__ import annotations

import logging
import sys
from typing import Optional


# ── tqdm-aware handler ────────────────────────────────────────────────────────

class _TqdmHandler(logging.StreamHandler):
    """
    Routes log records through tqdm.write() so that progress bars are not
    corrupted when a log line is printed mid-bar.
    Falls back to a plain StreamHandler write if tqdm is not installed.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            from tqdm import tqdm  # local import — tqdm is optional
            tqdm.write(self.format(record), file=sys.stdout)
        except ImportError:
            super().emit(record)
        except Exception:
            self.handleError(record)


# ── Shared formatter ──────────────────────────────────────────────────────────

_FORMATTER = logging.Formatter(
    fmt="%(asctime)s  %(levelname)-8s  %(name)-30s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_configured = False


# ── Public API ────────────────────────────────────────────────────────────────

def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure the root logger once.
    Safe to call multiple times — only the first call takes effect.

    Parameters
    ----------
    level:  Logging level (e.g. logging.DEBUG, logging.INFO).
    """
    global _configured
    if _configured:
        return

    root = logging.getLogger()
    root.setLevel(level)

    # Remove any handlers added automatically by basicConfig / third parties
    root.handlers.clear()

    handler = _TqdmHandler(sys.stdout)
    handler.setFormatter(_FORMATTER)
    root.addHandler(handler)

    # Quiet noisy third-party loggers
    for noisy in ("ultralytics", "PIL", "urllib3", "matplotlib"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Return a named logger.

    Calls setup_logging() automatically if it has not been called yet,
    so individual modules never need to call setup_logging() themselves.

    Parameters
    ----------
    name:   Typically __name__ of the calling module.
    level:  Optional override for this specific logger's level.
    """
    setup_logging()  # no-op if already configured
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger
