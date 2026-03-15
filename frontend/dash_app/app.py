"""Dash application factory and entry point."""

from __future__ import annotations

from pathlib import Path

import dash

from frontend.dash_app.layout import create_layout
from frontend.dash_app.callbacks import register_callbacks

_BG = "#272b30"
_ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder=str(_ASSETS_DIR),
    title="Onde Está o Waldo? IA",
    update_title=None,
)

# Override index_string so the reset runs before any Dash-injected CSS.
# This is the only reliable way to kill browser/Dash default margins.
app.index_string = f"""<!DOCTYPE html>
<html>
<head>
    {{%metas%}}
    <title>{{%title%}}</title>
    {{%favicon%}}
    <style>
      *, *::before, *::after {{ box-sizing: border-box; }}
      html, body {{
        margin: 0 !important;
        padding: 0 !important;
        background-color: {_BG} !important;
        overflow-x: hidden;
      }}
      /* Dash renderer containers */
      #react-entry-point,
      #_dash-app-content,
      #_dash-app-content > div {{
        background-color: {_BG} !important;
        min-height: 100vh;
      }}
    </style>
    {{%css%}}
</head>
<body>
    {{%app_entry%}}
    <footer>
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
    </footer>
</body>
</html>"""

app.layout = create_layout()
register_callbacks(app)
