"""Game page layout — the main Where is Waldo interactive scene."""

from __future__ import annotations

import plotly.graph_objects as go
from dash import dcc, html

from frontend.dash_app.layout import THEME, _card, _divider, _section_label

_T = THEME


def layout() -> html.Div:
    return html.Div(
        [
            # ── Left sidebar ──────────────────────────────────────────────────
            html.Div(
                [
                    _card(
                        [
                            _section_label("Dificuldade"),
                            dcc.RadioItems(
                                id="difficulty-radio",
                                options=[
                                    {
                                        "label": " Fácil   (20 personagens)",
                                        "value": "easy",
                                    },
                                    {
                                        "label": " Médio   (80 personagens)",
                                        "value": "medium",
                                    },
                                    {
                                        "label": " Difícil (150 personagens)",
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
                                "Gerar cena",
                                id="btn-generate",
                                n_clicks=0,
                                className="btn-primary",
                            ),
                        ]
                    ),
                    _card(
                        [
                            _section_label("Status"),
                            html.P(
                                id="status-text",
                                children="Gere uma cena para começar a jogar!",
                                style={
                                    "color": _T["text"],
                                    "fontSize": "14px",
                                    "lineHeight": "1.6",
                                    "margin": "0",
                                },
                            ),
                            _divider(),
                            html.Button(
                                "Enviar palpite",
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
                            _section_label("Legenda"),
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
                                    (_T["warning"], "Seu clique"),
                                    ("#5cb85c", "Aqui estava o Waldo"),
                                    (_T["primary"], "Detecção YOLO"),
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
                                "Nenhuma cena carregada",
                                style={
                                    "fontSize": "18px",
                                    "fontWeight": "600",
                                    "color": _T["text"],
                                    "marginBottom": "10px",
                                },
                            ),
                            html.Div(
                                "Selecione a dificuldade e clique em "
                                "Gerar cena para começar.",
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
