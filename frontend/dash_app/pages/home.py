"""Home / welcome page layout."""

from __future__ import annotations

from dash import dcc, html

from frontend.dash_app.layout import THEME, _card

_T = THEME


def _stat(value: str, label: str) -> html.Div:
    return html.Div(
        [
            html.Div(
                value,
                style={
                    "fontSize": "40px",
                    "fontWeight": "800",
                    "color": _T["text"],
                    "lineHeight": "1",
                },
            ),
            html.Div(
                label,
                style={
                    "fontSize": "13px",
                    "color": _T["text_muted"],
                    "marginTop": "4px",
                },
            ),
        ]
    )


def _how_step(title: str, desc: str) -> html.Div:
    return html.Div(
        [
            html.Div(
                title,
                style={
                    "fontSize": "15px",
                    "fontWeight": "700",
                    "color": _T["text"],
                    "marginBottom": "8px",
                },
            ),
            html.Div(
                desc,
                style={
                    "fontSize": "13px",
                    "color": _T["text_muted"],
                    "lineHeight": "1.6",
                    "textAlign": "center",
                },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "textAlign": "center",
            "flex": "1",
            "padding": "0 16px",
        },
    )


def layout() -> html.Div:
    return html.Div(
        [
            # ── Hero ─────────────────────────────────────────────────────────
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                "Onde Está o Waldo?",
                                style={
                                    "fontSize": "42px",
                                    "fontWeight": "800",
                                    "color": _T["text"],
                                },
                            ),
                            html.Span(
                                " IA",
                                style={
                                    "fontSize": "42px",
                                    "fontWeight": "300",
                                    "color": _T["primary"],
                                },
                            ),
                        ],
                        style={
                            "display": "inline-block",
                            "marginBottom": "16px",
                        },
                    ),
                    html.P(
                        "Gere uma cena, clique no Waldo e "
                        "veja se você consegue "
                        "achar antes do modelo YOLOv8 treinado do zero.",
                        style={
                            "fontSize": "16px",
                            "color": _T["text_muted"],
                            "maxWidth": "520px",
                            "lineHeight": "1.7",
                            "margin": "0 auto 24px",
                            "textAlign": "center",
                        },
                    ),
                ],
                style={
                    "textAlign": "center",
                    "padding": "32px 24px 24px",
                },
            ),

            html.Hr(
                style={
                    "border": "none",
                    "borderTop": f"1px solid {_T['border']}",
                    "margin": "0 auto",
                    "maxWidth": "700px",
                }
            ),

            # ── Info + Stats row ──────────────────────────────────────────────
            html.Div(
                [
                    # Project description
                    _card(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "O Projeto",
                                        style={
                                            "fontSize": "16px",
                                            "fontWeight": "700",
                                            "color": _T["text"],
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "marginBottom": "16px",
                                },
                            ),
                            html.P(
                                [
                                    "Um pipeline completo de ",
                                    html.Strong(
                                        "visão computacional",
                                        style={"color": _T["primary"]},
                                    ),
                                    " construído do zero: geração de dataset "
                                    "sintético, treinamento de YOLOv8 e "
                                    "inferência em tempo real via API.",
                                ],
                                style={
                                    "fontSize": "14px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.7",
                                    "margin": "0 0 12px 0",
                                },
                            ),
                            html.P(
                                "As cenas são geradas proceduralmente com "
                                "sprites pixel-art. O modelo aprende a "
                                "localizar o Waldo entre dezenas de "
                                "personagens similares.",
                                style={
                                    "fontSize": "14px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.7",
                                    "margin": "0",
                                },
                            ),
                        ],
                        extra_style={"flex": "2"},
                    ),

                    # Stats
                    _card(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "Dataset",
                                        style={
                                            "fontSize": "16px",
                                            "fontWeight": "700",
                                            "color": _T["text"],
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "marginBottom": "20px",
                                },
                            ),
                            html.Div(
                                [
                                    _stat("5 000", "cenas de treino"),
                                    html.Div(
                                        style={
                                            "width": "1px",
                                            "backgroundColor": _T["border"],
                                            "margin": "0 24px",
                                        }
                                    ),
                                    _stat("3", "dificuldades"),
                                    html.Div(
                                        style={
                                            "width": "1px",
                                            "backgroundColor": _T["border"],
                                            "margin": "0 24px",
                                        }
                                    ),
                                    _stat("500", "sprites únicos"),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                },
                            ),
                        ],
                        extra_style={"flex": "1"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "20px",
                    "maxWidth": "900px",
                    "margin": "16px auto",
                    "padding": "0 24px",
                    "alignItems": "stretch",
                },
            ),

            # ── How it works ──────────────────────────────────────────────────
            html.Div(
                [
                    html.P(
                        "COMO FUNCIONA",
                        style={
                            "color": _T["text_muted"],
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "letterSpacing": "2px",
                            "textAlign": "center",
                            "margin": "0 0 32px 0",
                        },
                    ),
                    html.Div(
                        [
                            _how_step(
                                "1. Geração da cena",
                                "Uma cena 640×640 é gerada proceduralmente "
                                "com sprites pixel-art e um fundo aleatório. "
                                "O Waldo é inserido em posição aleatória.",
                            ),
                            html.Div(
                                "→",
                                style={
                                    "fontSize": "24px",
                                    "color": _T["border"],
                                    "alignSelf": "center",
                                    "flexShrink": "0",
                                },
                            ),
                            _how_step(
                                "2. Seu palpite",
                                "Clique na imagem onde você acha que o Waldo "
                                "está. Você tem uma tentativa por cena.",
                            ),
                            html.Div(
                                "→",
                                style={
                                    "fontSize": "24px",
                                    "color": _T["border"],
                                    "alignSelf": "center",
                                    "flexShrink": "0",
                                },
                            ),
                            _how_step(
                                "3. IA detecta",
                                "O modelo YOLOv8 analisa a mesma cena e tenta "
                                "localizar o Waldo. Quem achou primeiro?",
                            ),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "flex-start",
                            "gap": "8px",
                        },
                    ),
                ],
                style={
                    "maxWidth": "900px",
                    "margin": "0 auto 48px",
                    "padding": "0 24px",
                },
            ),

            # ── CTA footer ────────────────────────────────────────────────────
            html.Div(
                [
                    dcc.Link(
                        html.Button(
                            "Jogar agora",
                            style={
                                "backgroundColor": _T["primary"],
                                "color": "#1a1d20",
                                "border": "none",
                                "borderRadius": "8px",
                                "padding": "14px 36px",
                                "fontSize": "16px",
                                "fontWeight": "700",
                                "cursor": "pointer",
                                "marginBottom": "12px",
                            },
                        ),
                        href="/game",
                    ),
                    html.Div(
                        [
                            "ou veja os ",
                            dcc.Link(
                                "detalhes técnicos",
                                href="/about",
                                style={
                                    "color": _T["primary"],
                                    "textDecoration": "none",
                                },
                            ),
                            " na página Sobre",
                        ],
                        style={
                            "fontSize": "13px",
                            "color": _T["text_muted"],
                        },
                    ),
                ],
                style={
                    "textAlign": "center",
                    "padding": "0 24px 48px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                },
            ),
        ],
        style={"backgroundColor": _T["bg"]},
    )
