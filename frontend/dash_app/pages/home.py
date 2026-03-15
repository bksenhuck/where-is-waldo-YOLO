"""Home / welcome page layout."""

from __future__ import annotations

from dash import dcc, html

from frontend.dash_app.layout import THEME, _card
from frontend.i18n import get_strings, t

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


def layout(lang: str = "pt") -> html.Div:
    s = get_strings(lang)

    return html.Div(
        [
            # ── Hero ─────────────────────────────────────────────────────
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                t(s, "home.hero.title"),
                                style={
                                    "fontSize": "42px",
                                    "fontWeight": "800",
                                    "color": _T["text"],
                                },
                            ),
                            html.Span(
                                t(s, "home.hero.accent"),
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
                        t(s, "home.hero.subtitle"),
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

            # ── Info + Stats row ──────────────────────────────────────────
            html.Div(
                [
                    _card(
                        [
                            html.Div(
                                html.Span(
                                    t(s, "home.project.title"),
                                    style={
                                        "fontSize": "16px",
                                        "fontWeight": "700",
                                        "color": _T["text"],
                                    },
                                ),
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "marginBottom": "16px",
                                },
                            ),
                            html.P(
                                [
                                    t(s, "home.project.body1_pre"),
                                    html.Strong(
                                        t(s, "home.project.body1_strong"),
                                        style={"color": _T["primary"]},
                                    ),
                                    t(s, "home.project.body1_post"),
                                ],
                                style={
                                    "fontSize": "14px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.7",
                                    "margin": "0 0 12px 0",
                                },
                            ),
                            html.P(
                                t(s, "home.project.body2"),
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

                    _card(
                        [
                            html.Div(
                                html.Span(
                                    t(s, "home.stats.title"),
                                    style={
                                        "fontSize": "16px",
                                        "fontWeight": "700",
                                        "color": _T["text"],
                                    },
                                ),
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "marginBottom": "20px",
                                },
                            ),
                            html.Div(
                                [
                                    _stat("5 000", t(s, "home.stats.scenes")),
                                    html.Div(style={
                                        "width": "1px",
                                        "backgroundColor": _T["border"],
                                        "margin": "0 24px",
                                    }),
                                    _stat("3", t(s, "home.stats.difficulties")),
                                    html.Div(style={
                                        "width": "1px",
                                        "backgroundColor": _T["border"],
                                        "margin": "0 24px",
                                    }),
                                    _stat("500", t(s, "home.stats.sprites")),
                                ],
                                style={"display": "flex", "alignItems": "center"},
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

            # ── How it works ──────────────────────────────────────────────
            html.Div(
                [
                    html.P(
                        t(s, "home.how.label"),
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
                                t(s, "home.how.step1.title"),
                                t(s, "home.how.step1.desc"),
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
                                t(s, "home.how.step2.title"),
                                t(s, "home.how.step2.desc"),
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
                                t(s, "home.how.step3.title"),
                                t(s, "home.how.step3.desc"),
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

            # ── CTA ───────────────────────────────────────────────────────
            html.Div(
                [
                    dcc.Link(
                        html.Button(
                            t(s, "home.cta.button"),
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
                            t(s, "home.cta.prefix"),
                            dcc.Link(
                                t(s, "home.cta.link_text"),
                                href="/about",
                                style={
                                    "color": _T["primary"],
                                    "textDecoration": "none",
                                },
                            ),
                            t(s, "home.cta.suffix"),
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
