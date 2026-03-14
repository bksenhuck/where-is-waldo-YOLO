"""Dash application factory and entry point."""

from __future__ import annotations

import dash

from frontend.dash_app.layout import create_layout
from frontend.dash_app.callbacks import register_callbacks

app = dash.Dash(
    __name__,
    # assets_folder is resolved relative to this file's package root
    suppress_callback_exceptions=True,
    title="Where is Waldo? AI",
    update_title=None,
)

app.layout = create_layout()
register_callbacks(app)
