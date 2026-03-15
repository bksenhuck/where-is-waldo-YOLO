"""About / technical details page layout."""

from __future__ import annotations

from dash import dcc, html

from frontend.dash_app.layout import THEME, _card
from frontend.i18n import get_strings, t

_T = THEME


def _tech_row(icon: str, name: str, desc: str) -> html.Div:
    return html.Div(
        [
            html.Span(
                icon,
                style={
                    "fontSize": "16px",
                    "fontWeight": "500",
                    "letterSpacing": "0.6px",
                    "minWidth": "72px",
                    "width": "72px",
                    "flexShrink": "0",
                    "lineHeight": "1.2",
                    "textAlign": "left",
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "color": _T["text_muted"],
                },
            ),
            html.Div(
                [
                    html.Span(
                        name,
                        style={
                            "fontSize": "14px",
                            "fontWeight": "700",
                            "color": _T["text"],
                        },
                    ),
                    html.Span(
                        f" — {desc}",
                        style={
                            "fontSize": "13px",
                            "color": _T["text_muted"],
                        },
                    ),
                ],
                style={"flex": "1", "minWidth": "0"},
            ),
        ],
        style={
            "display": "flex",
            "alignItems": "flex-start",
            "gap": "14px",
            "padding": "8px 0",
            "borderBottom": f"1px solid {_T['border']}",
        },
    )


def _pipeline_step(
    num: str,
    title: str,
    desc: str,
    cmd: str | None,
    accent: str,
) -> html.Div:
    cmd_block = html.Code(
        cmd,
        style={
            "fontSize": "12px",
            "backgroundColor": _T["surface2"],
            "color": _T["primary"],
            "padding": "4px 10px",
            "borderRadius": "4px",
            "fontFamily": "monospace",
        },
    ) if cmd else None

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        num,
                        style={
                            "width": "32px",
                            "height": "32px",
                            "borderRadius": "50%",
                            "backgroundColor": accent,
                            "color": "#1a1d20",
                            "fontWeight": "800",
                            "fontSize": "14px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "flexShrink": "0",
                        },
                    ),
                    html.Div(
                        [
                            html.Div(
                                title,
                                style={
                                    "fontSize": "14px",
                                    "fontWeight": "700",
                                    "color": _T["text"],
                                    "marginBottom": "4px",
                                },
                            ),
                            html.Div(
                                desc,
                                style={
                                    "fontSize": "13px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.6",
                                    "marginBottom": "8px",
                                },
                            ),
                            cmd_block,
                        ]
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "16px",
                    "alignItems": "flex-start",
                },
            )
        ],
        style={"padding": "16px 0"},
    )


def layout(lang: str = "pt") -> html.Div:
    s = get_strings(lang)
    return html.Div(
        [
            # ── Page title ────────────────────────────────────────────────────
            html.Div(
                [
                    html.H1(
                        t(s, "about.title"),
                        style={
                            "fontSize": "28px",
                            "fontWeight": "800",
                            "color": _T["text"],
                            "margin": "0 0 8px 0",
                        },
                    ),
                    html.P(
                        t(s, "about.subtitle"),
                        style={
                            "fontSize": "14px",
                            "color": _T["text_muted"],
                            "margin": "0",
                        },
                    ),
                ],
                style={"marginBottom": "32px"},
            ),

            # ── Row 1: Overview + Stack ────────────────────────────────────────
            html.Div(
                [
                    _card(
                        [
                            html.P(
                                t(s, "about.overview.label"),
                                style={
                                    "color": _T["text_muted"],
                                    "fontSize": "11px",
                                    "fontWeight": "700",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "1px",
                                    "margin": "0 0 16px 0",
                                },
                            ),
                            html.P(
                                [
                                    t(s, "about.overview.body1_pre"),
                                    html.Strong(
                                        t(s, "about.overview.body1_strong"),
                                        style={"color": _T["text"]},
                                    ),
                                    t(s, "about.overview.body1_suf"),
                                ],
                                style={
                                    "fontSize": "14px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.7",
                                    "margin": "0 0 12px 0",
                                },
                            ),
                            html.P(
                                t(s, "about.overview.body2"),
                                style={
                                    "fontSize": "14px",
                                    "color": _T["text_muted"],
                                    "lineHeight": "1.7",
                                    "margin": "0",
                                },
                            ),
                        ],
                        extra_style={"flex": "1"},
                    ),

                    _card(
                        [
                            html.P(
                                t(s, "about.stack.label"),
                                style={
                                    "color": _T["text_muted"],
                                    "fontSize": "11px",
                                    "fontWeight": "700",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "1px",
                                    "margin": "0 0 8px 0",
                                },
                            ),
                            _tech_row(
                                "ML", "YOLOv8n",
                                t(s, "about.tech.yolo.desc"),
                            ),
                            _tech_row(
                                "API", "FastAPI",
                                t(s, "about.tech.fastapi.desc"),
                            ),
                            _tech_row(
                                "UI", "Dash / Plotly",
                                t(s, "about.tech.dash.desc"),
                            ),
                            _tech_row(
                                "IMG", "Pillow",
                                t(s, "about.tech.pillow.desc"),
                            ),
                            _tech_row(
                                "PY", "Python 3.11",
                                t(s, "about.tech.python.desc"),
                            ),
                            html.Div(
                                _tech_row(
                                    "CLOUD", "Cloud Run + GCS",
                                    t(s, "about.tech.cloud.desc"),
                                ),
                                style={"borderBottom": "none"},
                            ),
                        ],
                        extra_style={"flex": "1"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "20px",
                    "marginBottom": "20px",
                    "alignItems": "stretch",
                },
            ),

            # ── Row 2: Pipeline ────────────────────────────────────────────────
            _card(
                [
                    html.P(
                        t(s, "about.pipeline.label"),
                        style={
                            "color": _T["text_muted"],
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "1px",
                            "margin": "0 0 8px 0",
                        },
                    ),
                    html.Div(
                        [
                            _pipeline_step(
                                "1",
                                t(s, "about.pipeline.step1.title"),
                                t(s, "about.pipeline.step1.desc"),
                                None,
                                _T["primary"],
                            ),
                            html.Div(
                                style={
                                    "borderLeft": (
                                        f"2px dashed {_T['border']}"
                                    ),
                                    "marginLeft": "15px",
                                    "height": "16px",
                                }
                            ),
                            _pipeline_step(
                                "2",
                                t(s, "about.pipeline.step2.title"),
                                t(s, "about.pipeline.step2.desc"),
                                None,
                                _T["success"],
                            ),
                            html.Div(
                                style={
                                    "borderLeft": (
                                        f"2px dashed {_T['border']}"
                                    ),
                                    "marginLeft": "15px",
                                    "height": "16px",
                                }
                            ),
                            _pipeline_step(
                                "3",
                                t(s, "about.pipeline.step3.title"),
                                t(s, "about.pipeline.step3.desc"),
                                None,
                                _T["warning"],
                            ),
                            html.Div(
                                style={
                                    "borderLeft": (
                                        f"2px dashed {_T['border']}"
                                    ),
                                    "marginLeft": "15px",
                                    "height": "16px",
                                }
                            ),
                            _pipeline_step(
                                "4",
                                t(s, "about.pipeline.step4.title"),
                                t(s, "about.pipeline.step4.desc"),
                                None,
                                _T["danger"],
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.Span(
                                t(s, "about.pipeline.footer"),
                                style={
                                    "fontSize": "13px",
                                    "color": _T["text_muted"],
                                },
                            ),
                        ],
                        style={
                            "marginTop": "16px",
                            "paddingTop": "16px",
                            "borderTop": f"1px solid {_T['border']}",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "10px",
                        },
                    ),
                ],
                extra_style={"marginBottom": "20px"},
            ),

            # ── Row 3: Architecture ────────────────────────────────────────────
            _card(
                [
                    html.P(
                        t(s, "about.arch.label"),
                        style={
                            "color": _T["text_muted"],
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "1px",
                            "margin": "0 0 16px 0",
                        },
                    ),
                    html.Div(
                        [
                            _arch_box(t(s, "about.arch.box1"), _T["surface2"]),
                            _arch_arrow(),
                            _arch_box(
                                "FastAPI\n/api/scene\n/api/detect",
                                _T["primary"],
                                dark=True,
                            ),
                            _arch_arrow(),
                            _arch_box(
                                t(s, "about.arch.box3"),
                                _T["surface2"],
                            ),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "8px",
                            "flexWrap": "wrap",
                        },
                    ),
                    html.P(
                        t(s, "about.arch.note"),
                        style={
                            "fontSize": "13px",
                            "color": _T["text_muted"],
                            "margin": "16px 0 0 0",
                            "lineHeight": "1.6",
                        },
                    ),
                ],
                extra_style={"marginBottom": "20px"},
            ),

            # ── Back to game ──────────────────────────────────────────────────
            html.Div(
                dcc.Link(
                    t(s, "about.back"),
                    href="/game",
                    style={
                        "color": _T["primary"],
                        "textDecoration": "none",
                        "fontSize": "14px",
                    },
                ),
                style={"paddingBottom": "8px"},
            ),
        ],
        style={
            "maxWidth": "900px",
            "margin": "0 auto",
            "padding": "40px 24px",
            "backgroundColor": _T["bg"],
        },
    )


def _arch_box(
    text: str,
    bg: str,
    dark: bool = False,
) -> html.Div:
    return html.Div(
        html.Pre(
            text,
            style={
                "margin": "0",
                "fontSize": "12px",
                "fontFamily": "monospace",
                "color": "#1a1d20" if dark else _T["text"],
                "textAlign": "center",
                "lineHeight": "1.6",
            },
        ),
        style={
            "backgroundColor": bg,
            "border": f"1px solid {_T['border']}",
            "borderRadius": "8px",
            "padding": "12px 20px",
            "minWidth": "120px",
        },
    )


def _arch_arrow() -> html.Div:
    return html.Div(
        "→",
        style={
            "fontSize": "20px",
            "color": _T["text_muted"],
            "flexShrink": "0",
        },
    )
