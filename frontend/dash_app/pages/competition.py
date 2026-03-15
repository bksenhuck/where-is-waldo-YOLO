"""Competition page — 5-round hard-difficulty Waldo vs YOLO challenge."""

from __future__ import annotations

import plotly.graph_objects as go
from dash import dcc, html

from frontend.dash_app.layout import THEME, _card, _section_label
from frontend.i18n import get_strings, t

_T = THEME
TOTAL_ROUNDS = 5


def layout(lang: str = "pt") -> html.Div:
    """Return the competition page layout (static skeleton; dynamic parts driven by callbacks)."""
    s = get_strings(lang)

    return html.Div(
        [
            html.Div(
                [
                    # ── Header row: timer (left) + round/scoreboard (center) + actions (right) ─
                    html.Div(
                        [
                            html.Div(
                                id="comp-timer-display",
                                style={"flex": "1"},
                            ),
                            html.Div(
                                id="comp-header",
                                style={"flex": "1"},
                            ),
                            # Wrapper always participates in flex layout (same
                            # pattern as timer/header wrappers above).
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Button(
                                                t(s, "comp.btn.submit"),
                                                id="comp-btn-submit",
                                                n_clicks=0,
                                                disabled=True,
                                                className="btn-secondary",
                                                style={"width": "100%", "marginBottom": "10px", "display": "none"},
                                            ),
                                            html.Button(
                                                t(s, "comp.btn.next"),
                                                id="comp-btn-next",
                                                n_clicks=0,
                                                disabled=True,
                                                className="btn-primary",
                                                style={"width": "100%", "display": "none"},
                                            ),
                                        ],
                                        id="comp-action-card",
                                        style={"display": "none"},
                                    ),
                                ],
                                style={"flex": "1", "display": "flex"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "16px",
                            "alignItems": "stretch",
                            "marginBottom": "16px",
                        },
                    ),

                    # ── Start screen (hidden once competition begins) ─────────
                    html.Div(
                        id="comp-start-screen",
                        children=_start_screen_content(lang),
                    ),

                    # ── Game area (shown after competition starts) ────────────
                    html.Div(
                        [
                            # Placeholder shown while scene is being generated
                            html.Div(
                                id="comp-graph-placeholder",
                                children=[
                                    html.Div(
                                        t(s, "comp.placeholder.title"),
                                        style={
                                            "fontSize": "18px",
                                            "fontWeight": "600",
                                            "color": _T["text"],
                                            "marginBottom": "10px",
                                        },
                                    ),
                                ],
                                style={
                                    "height": "640px",
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "backgroundColor": _T["surface"],
                                    "border": f"1px solid {_T['border']}",
                                    "borderRadius": "10px",
                                    "textAlign": "center",
                                    "padding": "24px",
                                },
                            ),
                            # Scene graph (hidden until scene loaded)
                            html.Div(
                                _card(
                                    [
                                        dcc.Loading(
                                            id="comp-loading-scene",
                                            type="circle",
                                            color=_T["primary"],
                                            children=dcc.Graph(
                                                id="comp-scene-graph",
                                                figure=go.Figure(),
                                                config={
                                                    "displayModeBar": False,
                                                    "scrollZoom": False,
                                                    "displaylogo": False,
                                                    "staticPlot": False,
                                                },
                                                style={"height": "640px"},
                                            ),
                                        )
                                    ],
                                    extra_style={"padding": "12px"},
                                ),
                                id="comp-graph-card",
                                style={"display": "none"},
                            ),
                            # Round result panel
                            html.Div(id="comp-result-panel", style={"marginTop": "8px"}),
                        ],
                        id="comp-graph-wrapper",
                        style={"display": "none"},
                    ),

                    # ── Final screen (shown after all rounds complete) ─────────
                    html.Div(
                        [
                            html.Div(id="comp-final-content"),
                            # Static "Play again" button — always inside final screen
                            html.Div(
                                html.Button(
                                    t(s, "comp.btn.play_again"),
                                    id="comp-btn-restart",
                                    n_clicks=0,
                                    className="btn-secondary",
                                    style={"fontSize": "16px", "padding": "12px 0", "width": "100%"},
                                ),
                                style={"maxWidth": "360px", "margin": "24px auto 0 auto"},
                            ),
                        ],
                        id="comp-final-screen",
                        style={"display": "none"},
                    ),
                ],
                style={
                    "maxWidth": "1100px",
                    "margin": "0 auto",
                    "padding": "24px",
                },
            )
        ],
    )


def _start_screen_content(lang: str = "pt") -> list:
    """Initial splash screen shown before competition starts."""
    s = get_strings(lang)
    rules = [
        ("1.", t(s, "comp.rules.rule1")),
        ("2.", t(s, "comp.rules.rule2")),
        ("3.", t(s, "comp.rules.rule3")),
        ("4.", t(s, "comp.rules.rule4")),
    ]

    return [
        html.Div(
            [
                html.H1(
                    t(s, "comp.title"),
                    style={
                        "color": _T["text"],
                        "fontSize": "32px",
                        "fontWeight": "800",
                        "textAlign": "center",
                        "margin": "0 0 8px 0",
                    },
                ),
                html.P(
                    t(s, "comp.subtitle"),
                    style={
                        "color": _T["text_muted"],
                        "fontSize": "16px",
                        "textAlign": "center",
                        "margin": "0 0 32px 0",
                    },
                ),
                _card(
                    [
                        _section_label(t(s, "comp.rules.label")),
                        *[
                            html.Div(
                                [
                                    html.Span(
                                        icon,
                                        style={
                                            "fontSize": "20px",
                                            "marginRight": "12px",
                                            "flexShrink": "0",
                                        },
                                    ),
                                    html.Span(
                                        text,
                                        style={
                                            "color": _T["text"],
                                            "fontSize": "14px",
                                            "lineHeight": "1.6",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "flex-start",
                                    "marginBottom": "12px",
                                },
                            )
                            for icon, text in rules
                        ],
                    ],
                    extra_style={"maxWidth": "500px", "margin": "0 auto 32px auto"},
                ),
                html.Div(
                    html.Button(
                        t(s, "comp.btn.start"),
                        id="comp-btn-start",
                        n_clicks=0,
                        className="btn-secondary",
                        style={"fontSize": "16px", "padding": "12px 0", "width": "100%"},
                    ),
                    style={"maxWidth": "500px", "margin": "0 auto"},
                ),
            ],
            style={"padding": "40px 0"},
        )
    ]
