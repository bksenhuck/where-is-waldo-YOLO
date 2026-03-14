"""Layout definition for the Where is Waldo Dash application."""

from __future__ import annotations

from dash import dcc, html

# ── Dark theme palette — single source of truth for all Dash modules ──────────
THEME = {
    "bg":           "#272b30",
    "surface":      "#3a3f44",
    "surface2":     "#484e55",
    "border":       "#484e55",
    "text":         "#aab3bc",
    "text_muted":   "#7a8288",
    "primary":      "#5bc0de",
    "success":      "#5cb85c",
    "warning":      "#f0ad4e",
    "danger":       "#d9534f",
}
_T = THEME  # local shorthand


def _card(children: list, extra_style: dict | None = None) -> html.Div:
    style = {
        "backgroundColor": _T["surface"],
        "border": f"1px solid {_T['border']}",
        "borderRadius": "10px",
        "padding": "20px",
    }
    if extra_style:
        style.update(extra_style)
    return html.Div(children, style=style)


def _section_label(text: str) -> html.P:
    return html.P(
        text,
        style={
            "color": _T["text_muted"],
            "fontSize": "11px",
            "fontWeight": "700",
            "textTransform": "uppercase",
            "letterSpacing": "1px",
            "margin": "0 0 8px 0",
        },
    )


def _divider() -> html.Hr:
    return html.Hr(
        style={
            "border": "none",
            "borderTop": f"1px solid {_T['border']}",
            "margin": "20px 0",
        }
    )


def create_layout() -> html.Div:
    """Build and return the full application layout."""

    return html.Div(
        [
            # ── Stores ──────────────────────────────────────────────────────
            dcc.Store(id="store-scene"),   # scene image + waldo bbox
            dcc.Store(id="store-click"),   # user click {x, y} or null
            dcc.Store(id="store-result"),  # detection result dict or null

            # ── Header ──────────────────────────────────────────────────────
            html.Header(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "🔍",
                                    style={"fontSize": "26px", "marginRight": "10px"},
                                ),
                                html.Span(
                                    "Where is Waldo?",
                                    style={
                                        "fontSize": "22px",
                                        "fontWeight": "800",
                                        "color": _T["text"],
                                    },
                                ),
                                html.Span(
                                    " AI Challenge",
                                    style={
                                        "fontSize": "22px",
                                        "fontWeight": "300",
                                        "color": _T["primary"],
                                    },
                                ),
                            ],
                            style={"display": "flex", "alignItems": "center"},
                        ),
                        html.P(
                            "Can you spot Waldo faster than the AI?",
                            style={
                                "color": _T["text_muted"],
                                "fontSize": "13px",
                                "margin": "0",
                            },
                        ),
                    ],
                    style={
                        "maxWidth": "1440px",
                        "margin": "0 auto",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                    },
                ),
                style={
                    "backgroundColor": _T["surface"],
                    "borderBottom": f"1px solid {_T['border']}",
                    "padding": "14px 24px",
                    "position": "sticky",
                    "top": "0",
                    "zIndex": "100",
                },
            ),

            # ── Main content ─────────────────────────────────────────────────
            html.Div(
                [
                    # ── Left sidebar: controls ───────────────────────────────
                    html.Div(
                        [
                            # Difficulty
                            _card(
                                [
                                    _section_label("Difficulty"),
                                    dcc.RadioItems(
                                        id="difficulty-radio",
                                        options=[
                                            {"label": " Easy  (20 chars)",   "value": "easy"},
                                            {"label": " Medium (80 chars)",  "value": "medium"},
                                            {"label": " Hard  (150 chars)",  "value": "hard"},
                                        ],
                                        value="medium",
                                        inputStyle={"marginRight": "8px"},
                                        labelStyle={
                                            "display": "block",
                                            "marginBottom": "10px",
                                            "color": _T["text"],
                                            "fontSize": "14px",
                                            "cursor": "pointer",
                                        },
                                        className="radio-group",
                                    ),
                                    _divider(),
                                    html.Button(
                                        "⚡ Generate Scene",
                                        id="btn-generate",
                                        n_clicks=0,
                                        className="btn-primary",
                                    ),
                                ]
                            ),

                            # Status
                            _card(
                                [
                                    _section_label("Status"),
                                    html.P(
                                        id="status-text",
                                        children="Generate a scene to start playing!",
                                        style={
                                            "color": _T["text"],
                                            "fontSize": "14px",
                                            "lineHeight": "1.6",
                                            "margin": "0",
                                        },
                                    ),
                                    _divider(),
                                    html.Button(
                                        "✔ Submit My Guess",
                                        id="btn-submit",
                                        n_clicks=0,
                                        disabled=True,
                                        className="btn-secondary",
                                    ),
                                ],
                                extra_style={"marginTop": "16px"},
                            ),

                            # Result panel
                            html.Div(
                                id="result-panel",
                                style={"marginTop": "16px"},
                            ),

                            # Legend
                            _card(
                                [
                                    _section_label("Legend"),
                                    *[
                                        html.Div(
                                            [
                                                html.Span(
                                                    "■",
                                                    style={
                                                        "color": color,
                                                        "fontSize": "18px",
                                                        "marginRight": "8px",
                                                    },
                                                ),
                                                html.Span(
                                                    label,
                                                    style={
                                                        "color": _T["text"],
                                                        "fontSize": "13px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "marginBottom": "6px",
                                            },
                                        )
                                        for color, label in [
                                            (_T["warning"], "Your click"),
                                            ("#5cb85c", "Ground truth"),
                                            (_T["primary"], "YOLO detection"),
                                        ]
                                    ],
                                ],
                                extra_style={"marginTop": "16px"},
                            ),
                        ],
                        style={
                            "width": "270px",
                            "flexShrink": "0",
                            "display": "flex",
                            "flexDirection": "column",
                        },
                    ),

                    # ── Right: scene graph ───────────────────────────────────
                    html.Div(
                        [
                            _card(
                                [
                                    dcc.Loading(
                                        id="loading-scene",
                                        type="circle",
                                        color=_T["primary"],
                                        children=dcc.Graph(
                                            id="scene-graph",
                                            config={
                                                "displayModeBar": True,
                                                "modeBarButtonsToRemove": [
                                                    "select2d",
                                                    "lasso2d",
                                                    "autoScale2d",
                                                ],
                                                "scrollZoom": True,
                                                "displaylogo": False,
                                                "toImageButtonOptions": {
                                                    "format": "png",
                                                    "filename": "waldo_scene",
                                                },
                                            },
                                            style={"height": "640px"},
                                        ),
                                    )
                                ],
                                extra_style={"padding": "12px"},
                            )
                        ],
                        style={"flex": "1", "minWidth": "0"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "20px",
                    "maxWidth": "1440px",
                    "margin": "24px auto",
                    "padding": "0 24px",
                    "alignItems": "flex-start",
                },
            ),
        ],
        style={
            "backgroundColor": _T["bg"],
            "minHeight": "100vh",
            "fontFamily": "'Inter', 'Segoe UI', system-ui, sans-serif",
            "color": _T["text"],
        },
    )
