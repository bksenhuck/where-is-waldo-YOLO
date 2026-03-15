"""Shell layout — fixed header/footer + page routing container."""

from __future__ import annotations

from dash import dcc, html

# ── Dark theme palette ───────────────────────────────────────────────────
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
_T = THEME

_NAV_H = "52px"
_FOOT_H = "34px"

_NAV_LINKS = [
    ("Início",  "/"),
    ("Jogar", "/game"),
    ("Sobre", "/about"),
]


# ── Shared component helpers (imported by page modules) ──────────────────

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


def _nav_link(label: str, href: str) -> dcc.Link:
    return dcc.Link(
        label,
        href=href,
        id=f"nav-{label.lower()}",
        style={
            "color": _T["text_muted"],
            "textDecoration": "none",
            "fontSize": "14px",
            "fontWeight": "500",
            "padding": "4px 0",
        },
    )


def create_layout() -> html.Div:
    """Shell with fixed header, routed content area, and fixed footer."""

    return html.Div(
        [
            dcc.Location(id="url", refresh=False),

            # ── Stores (game state — always present) ─────────────────────
            dcc.Store(id="store-scene"),
            dcc.Store(id="store-click"),
            dcc.Store(id="store-result"),
            dcc.Store(id="store-generate-click", data=0),
            # Incremented every time the user enters /game — guarantees
            # the render callback fires even when the scene stores are
            # already None (so graph-card is always hidden on entry).
            dcc.Store(id="store-game-nav", data=0),

            # ── Fixed header ─────────────────────────────────────────────────
            html.Header(
                html.Div(
                    [
                        # Logo
                        dcc.Link(
                            html.Div(
                                [
                                    html.Span(
                                        "Onde Está o Waldo?",
                                        style={
                                            "fontSize": "18px",
                                            "fontWeight": "800",
                                            "color": _T["text"],
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                },
                            ),
                            href="/",
                            style={"textDecoration": "none"},
                        ),

                        # Nav links
                        html.Nav(
                            [
                                _nav_link(label, href)
                                for label, href in _NAV_LINKS
                            ],
                            style={
                                "display": "flex",
                                "gap": "28px",
                                "alignItems": "center",
                            },
                        ),
                    ],
                    style={
                        "maxWidth": "1440px",
                        "margin": "0 auto",
                        "padding": "0 24px",
                        "height": "100%",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                    },
                ),
                style={
                    "position": "fixed",
                    "top": "0",
                    "left": "0",
                    "right": "0",
                    "height": _NAV_H,
                    "zIndex": "1000",
                    "backgroundColor": _T["surface"],
                    "borderBottom": f"1px solid {_T['border']}",
                },
            ),

            # ── Pages — all always mounted, visibility toggled by URL ────
            html.Main(
                [
                    html.Div(id="page-home"),
                    html.Div(id="page-game", style={"display": "none"}),
                    html.Div(id="page-about", style={"display": "none"}),
                ],
                style={
                    "paddingTop": _NAV_H,
                    "paddingBottom": _FOOT_H,
                    "minHeight": "100vh",
                    "backgroundColor": _T["bg"],
                },
            ),

            # ── Fixed footer ─────────────────────────────────────────────────
            html.Footer(
                html.Span(
                    "Onde Está o Waldo? - Desafio de IA",
                    style={
                        "color": _T["text_muted"],
                        "fontSize": "12px",
                    },
                ),
                style={
                    "position": "fixed",
                    "bottom": "0",
                    "left": "0",
                    "right": "0",
                    "height": _FOOT_H,
                    "zIndex": "1000",
                    "backgroundColor": _T["surface"],
                    "borderTop": f"1px solid {_T['border']}",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
            ),
        ],
        style={
            "backgroundColor": _T["bg"],
            "fontFamily": "'Inter', 'Segoe UI', system-ui, sans-serif",
            "color": _T["text"],
        },
    )
