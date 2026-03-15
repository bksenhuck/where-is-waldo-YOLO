"""Game page layout — the main Where is Waldo interactive scene."""

from __future__ import annotations

import plotly.graph_objects as go
from dash import dcc, html

from frontend.dash_app.layout import THEME, _card, _divider, _section_label
from frontend.i18n import get_strings, t

_T = THEME


def layout(lang: str = "pt") -> html.Div:
    s = get_strings(lang)
    return html.Div(
        [
            # ── Left sidebar ──────────────────────────────────────────────────
            html.Div(
                [
                    _card(
                        [
                            _section_label(t(s, "game.difficulty.label")),
                            dcc.RadioItems(
                                id="difficulty-radio",
                                options=[
                                    {
                                        "label": " " + t(s, "game.difficulty.easy"),
                                        "value": "easy",
                                    },
                                    {
                                        "label": " " + t(s, "game.difficulty.medium"),
                                        "value": "medium",
                                    },
                                    {
                                        "label": " " + t(s, "game.difficulty.hard"),
                                        "value": "hard",
                                    },
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
                                t(s, "game.btn.generate"),
                                id="btn-generate",
                                n_clicks=0,
                                className="btn-primary",
                            ),
                        ]
                    ),
                    _card(
                        [
                            _section_label(t(s, "game.status.label")),
                            html.P(
                                id="status-text",
                                children=t(s, "game.status.idle"),
                                style={
                                    "color": _T["text"],
                                    "fontSize": "14px",
                                    "lineHeight": "1.6",
                                    "margin": "0",
                                },
                            ),
                            _divider(),
                            html.Button(
                                t(s, "game.btn.submit"),
                                id="btn-submit",
                                n_clicks=0,
                                disabled=True,
                                className="btn-secondary",
                            ),
                        ],
                        extra_style={"marginTop": "16px"},
                    ),
                    _card(
                        [
                            _section_label(t(s, "game.legend.label")),
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
                                    (_T["warning"], t(s, "game.legend.click")),
                                    ("#5cb85c", t(s, "game.legend.waldo")),
                                    (_T["primary"], t(s, "game.legend.yolo")),
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

            # ── Scene graph ───────────────────────────────────────────────────
            html.Div(
                [
                    # Placeholder — shown when no scene is loaded
                    html.Div(
                        id="graph-placeholder",
                        children=[
                            html.Div(
                                t(s, "game.placeholder.title"),
                                style={
                                    "fontSize": "18px",
                                    "fontWeight": "600",
                                    "color": _T["text"],
                                    "marginBottom": "10px",
                                },
                            ),
                            html.Div(
                                t(s, "game.placeholder.body"),
                                style={
                                    "fontSize": "14px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.6",
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
                    # Graph — hidden until a scene is loaded
                    html.Div(
                        _card(
                            [
                                dcc.Loading(
                                    id="loading-scene",
                                    type="circle",
                                    color=_T["primary"],
                                    children=dcc.Graph(
                                        id="scene-graph",
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
                        id="graph-card",
                        style={"display": "none"},
                    ),
                    # Results — shown below the graph after submission
                    html.Div(
                        id="result-panel",
                        style={"marginTop": "8px"},
                    ),
                ],
                style={"flex": "1", "minWidth": "0"},
            ),
        ],
        style={
            "display": "flex",
            "gap": "20px",
            "maxWidth": "1440px",
            "margin": "0 auto",
            "padding": "24px 24px",
            "alignItems": "flex-start",
        },
    )
