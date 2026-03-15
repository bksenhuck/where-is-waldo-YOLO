"""Dash callback definitions for the Where is Waldo application."""

from __future__ import annotations

import base64
import io
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash import Input, Output, State, html, no_update
from PIL import Image

from backend.utils.bbox_utils import point_in_bbox
from config.settings import API_BASE, INTERNAL_API_KEY

# ── Palette — single source of truth lives in layout.py ──────────────────────
from frontend.dash_app.layout import THEME as _T
from frontend.i18n import get_strings, t

_BG = _T["bg"]
_SURFACE = _T["surface"]
_TEXT = _T["text"]
_TEXT_MUTED = _T["text_muted"]
_PRIMARY = _T["primary"]
_SUCCESS = _T["success"]
_WARNING = _T["warning"]
_DANGER = _T["danger"]


# ── Image helpers ─────────────────────────────────────────────────────────

def _b64_to_pil(b64: str) -> Image.Image:
    """Decode base64 PNG string to PIL image."""
    data = base64.b64decode(b64)
    return Image.open(io.BytesIO(data)).convert("RGB")


def _apply_spotlight_mask(
    arr: np.ndarray,
    waldo_bbox: Tuple[int, int, int, int],
) -> np.ndarray:
    """Darken scene outside Waldo bbox using pixel-level blending."""

    h, w = arr.shape[:2]
    x1, y1, x2, y2 = waldo_bbox

    x1 = max(0, min(w - 1, int(x1)))
    y1 = max(0, min(h - 1, int(y1)))
    x2 = max(0, min(w, int(x2)))
    y2 = max(0, min(h, int(y2)))

    if x2 <= x1 or y2 <= y1:
        return arr

    masked = arr.astype(np.float32)
    # Near-blackout outside bbox
    masked *= 0.22
    # Keep Waldo area fully visible
    masked[y1:y2, x1:x2] = arr[y1:y2, x1:x2]
    return np.clip(masked, 0, 255).astype(np.uint8)


# ── Figure builders ───────────────────────────────────────────────────────

def _empty_figure() -> go.Figure:
    """Placeholder figure shown before first scene is generated."""
    fig = go.Figure()
    fig.add_annotation(
        text="Clique em <b>⚡ Gerar cena</b> para começar o jogo!",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=18, color=_TEXT_MUTED, family="Inter"),
    )
    fig.update_layout(
        paper_bgcolor=_SURFACE,
        plot_bgcolor=_SURFACE,
        margin=dict(l=0, r=0, t=0, b=0),
        height=640,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def _scene_figure(
    img: Image.Image,
    click: Optional[Dict[str, float]] = None,
    waldo_bbox: Optional[Tuple[int, int, int, int]] = None,
    yolo_bbox: Optional[Tuple[int, int, int, int]] = None,
    show_truth: bool = False,
) -> go.Figure:
    """
    Build the main interactive scene figure.

    Parameters
    ----------
    img:         PIL scene image.
    click:       Dict with {x, y} pixel coordinates of user click (or None).
    waldo_bbox:  Ground-truth Waldo bbox (x1,y1,x2,y2) in pixels.
    yolo_bbox:   YOLO top-detection bbox (x1,y1,x2,y2) in pixels (or None).
    show_truth:  When True, overlay all bboxes and reveal ground truth.
    """
    arr = np.array(img)
    if show_truth and waldo_bbox:
        arr = _apply_spotlight_mask(arr, waldo_bbox)
    h, w = arr.shape[:2]

    # Base image figure — px.imshow gives proper pixel-space coordinates
    fig = px.imshow(arr, binary_backend="jpg")
    fig.update_traces(hovertemplate="x: %{x}<br>y: %{y}<extra></extra>")

    shapes: List[dict] = []
    annotations: List[dict] = []
    scatter_traces: List[go.Scatter] = []

    if click:
        cx, cy = float(click["x"]), float(click["y"])
        scatter_traces.append(
            go.Scatter(
                x=[cx],
                y=[cy],
                mode="markers",
                marker=dict(
                    symbol="x",
                    size=20,
                    color=_WARNING,
                    line=dict(width=4, color=_WARNING),
                ),
                name="Seu clique",
                showlegend=False,
            )
        )
        if show_truth:
            annotations.append(
                dict(
                    x=cx,
                    y=max(0, cy - 10),
                    text="<b>Seu clique</b>",
                    showarrow=False,
                    font=dict(color=_WARNING, size=12),
                    bgcolor="rgba(0,0,0,0.65)",
                    xanchor="center",
                    yanchor="bottom",
                )
            )

    if show_truth:
        # ── Ground-truth box (green) ───────────────────────────────────
        if waldo_bbox:
            x1, y1, x2, y2 = waldo_bbox
            shapes.append(
                dict(
                    type="rect",
                    x0=x1, y0=y1, x1=x2, y1=y2,
                    line=dict(color=_SUCCESS, width=4),
                    fillcolor="rgba(120,220,140,0.20)",
                )
            )
            annotations.append(
                dict(
                    x=x1,
                    y=max(0, y1 - 6),
                    text="<b>Aqui estava o Waldo</b>",
                    showarrow=False,
                    font=dict(color=_SUCCESS, size=12),
                    bgcolor="rgba(0,0,0,0.65)",
                    xanchor="left",
                    yanchor="bottom",
                )
            )

        # ── YOLO detection box (blue) ──────────────────────────────────
        if yolo_bbox:
            x1, y1, x2, y2 = yolo_bbox
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            shapes.append(
                dict(
                    type="rect",
                    x0=x1, y0=y1, x1=x2, y1=y2,
                    line=dict(color=_PRIMARY, width=3),
                    fillcolor="rgba(91,192,222,0.12)",
                )
            )
            annotations.append(
                dict(
                    x=x2,
                    y=max(0, y1 - 6),
                    text="<b>IA (YOLO)</b>",
                    showarrow=False,
                    font=dict(color=_PRIMARY, size=12),
                    bgcolor="rgba(0,0,0,0.65)",
                    xanchor="right",
                    yanchor="bottom",
                )
            )
            scatter_traces.append(
                go.Scatter(
                    x=[mx],
                    y=[my],
                    mode="markers",
                    marker=dict(
                        symbol="diamond",
                        size=12,
                        color=_PRIMARY,
                        line=dict(width=2, color="#ffffff"),
                    ),
                    name="Modelo (YOLO)",
                    showlegend=False,
                )
            )
            annotations.append(
                dict(
                    x=mx,
                    y=min(h - 1, my + 12),
                    text="<b>Modelo (YOLO)</b>",
                    showarrow=False,
                    font=dict(color=_PRIMARY, size=12),
                    bgcolor="rgba(0,0,0,0.65)",
                    xanchor="center",
                    yanchor="top",
                )
            )

    for trace in scatter_traces:
        fig.add_trace(trace)

    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        margin=dict(l=0, r=0, t=0, b=0),
        height=640,
        shapes=shapes,
        annotations=annotations,
        xaxis=dict(
            range=[-0.5, w - 0.5],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            fixedrange=True,
        ),
        yaxis=dict(
            range=[h - 0.5, -0.5],  # top-down image orientation
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            scaleanchor="x",
            fixedrange=True,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            font=dict(color=_TEXT, size=12),
            bgcolor="rgba(58,63,68,0.85)",
            bordercolor=_SURFACE,
            borderwidth=1,
        ),
        dragmode=False,
        uirevision="static",  # preserves zoom/pan across re-renders
    )

    return fig


# ── Result panel ───────────────────────────────────────────────────────────

def _result_card(children: list) -> html.Div:
    return html.Div(
        children,
        className="result-panel",
        style={
            "backgroundColor": _SURFACE,
            "border": f"1px solid {_SUCCESS}40",
            "borderRadius": "10px",
            "padding": "12px 18px",
        },
    )


def _result_row(icon: str, label: str, message: str, color: str) -> html.Div:
    return html.Div(
        [
            html.Span(icon, style={"fontSize": "22px", "marginRight": "10px"}),
            html.Div(
                [
                    html.Span(
                        label,
                        style={
                            "color": _TEXT_MUTED,
                            "fontSize": "11px",
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "1px",
                            "display": "block",
                        },
                    ),
                    html.Span(
                        message,
                        style={
                            "color": color,
                            "fontSize": "15px",
                            "fontWeight": "600",
                        },
                    ),
                ]
            ),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "marginBottom": "14px",
        },
    )


def _build_result_panel(result: Dict[str, Any], lang: str = "pt") -> html.Div:
    """Render the result card after submission."""
    s = get_strings(lang)
    user_found: bool = result["user_found"]
    yolo_found: bool = result["yolo_found"]
    yolo_conf: Optional[float] = result.get("yolo_conf")

    user_msg = (
        t(s, "result.you.found")
        if user_found
        else t(s, "result.you.missed")
    )
    user_color = _SUCCESS if user_found else _DANGER

    if yolo_found and yolo_conf is not None:
        yolo_msg = t(s, "result.yolo.found", conf=f"{yolo_conf:.0%}")
    elif yolo_found:
        yolo_msg = t(s, "result.yolo.found_nc")
    else:
        yolo_msg = t(s, "result.yolo.missed")
    yolo_color = _SUCCESS if yolo_found else _DANGER

    # Verdict
    if user_found and yolo_found:
        verdict = t(s, "result.verdict.both")
        verdict_color = _SUCCESS
    elif user_found:
        verdict = t(s, "result.verdict.user")
        verdict_color = _WARNING
    elif yolo_found:
        verdict = t(s, "result.verdict.yolo")
        verdict_color = _PRIMARY
    else:
        verdict = t(s, "result.verdict.none")
        verdict_color = _TEXT_MUTED

    col_you = t(s, "result.col.you")
    col_yolo = t(s, "result.col.yolo")
    col_result = t(s, "result.col.result")

    def _col(label, icon, message, color):
        return html.Div(
            [
                html.Span(
                    label,
                    style={
                        "color": _TEXT_MUTED,
                        "fontSize": "11px",
                        "fontWeight": "700",
                        "textTransform": "uppercase",
                        "letterSpacing": "1px",
                        "display": "block",
                        "marginBottom": "3px",
                    },
                ),
                html.Div(
                    [
                        *(
                            [html.Span(
                                icon,
                                style={
                                    "fontSize": "16px",
                                    "fontWeight": "700",
                                    "color": color,
                                    "marginRight": "6px",
                                },
                            )]
                            if icon else []
                        ),
                        html.Span(
                            message,
                            style={
                                "color": color,
                                "fontSize": "15px",
                                "fontWeight": "600",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                ),
            ],
            style={"flex": "1", "textAlign": "center"},
        )

    def _divider():
        return html.Div(style={
            "width": "1px",
            "backgroundColor": f"{_TEXT_MUTED}40",
            "alignSelf": "stretch",
        })

    return _result_card(
        [
            html.Div(
                [
                    _col(
                        col_you,
                        "+" if user_found else "−",
                        user_msg,
                        user_color,
                    ),
                    _divider(),
                    _col(
                        col_yolo,
                        "+" if yolo_found else "−",
                        yolo_msg,
                        yolo_color,
                    ),
                    _divider(),
                    _col(col_result, "", verdict, verdict_color),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
        ]
    )


# ── Callback registration ─────────────────────────────────────────────────

def register_callbacks(app) -> None:
    """Register all Dash callbacks onto the app instance."""

    # ── CB0: Page routing ──────────────────────────────────────────────
    from frontend.dash_app.pages import home, game, about, competition, model

    _show = {"display": "block"}
    _hide = {"display": "none"}

    @app.callback(
        Output("page-home", "children"),
        Output("page-home", "style"),
        Output("page-game", "children"),
        Output("page-game", "style"),
        Output("page-about", "children"),
        Output("page-about", "style"),
        Output("page-competition", "children"),
        Output("page-competition", "style"),
        Output("page-model", "children"),
        Output("page-model", "style"),
        Output("store-scene", "data", allow_duplicate=True),
        Output("store-click", "data", allow_duplicate=True),
        Output("store-result", "data", allow_duplicate=True),
        Output("store-generate-click", "data", allow_duplicate=True),
        Output("store-game-nav", "data"),
        Input("url", "pathname"),
        State("page-home", "children"),
        State("page-about", "children"),
        State("store-game-nav", "data"),
        State("lang-store", "data"),
        prevent_initial_call="initial_duplicate",
    )
    def route(pathname, home_children, about_children, nav_count, lang):
        # Home and About are lazy-loaded (no stateful components to reset).
        # Game and Competition are always recreated fresh on every visit.
        lang = lang or "pt"
        new_home = home_children or home.layout(lang)
        new_about = about_children or about.layout(lang)
        nav = (nav_count or 0) + 1

        if pathname == "/game":
            return (
                new_home, _hide,
                game.layout(lang), _show,
                new_about, _hide,
                no_update, _hide,
                no_update, _hide,
                None, None, None, 0, nav,
            )
        if pathname == "/competition":
            return (
                new_home, _hide,
                no_update, _hide,
                new_about, _hide,
                competition.layout(lang), _show,
                no_update, _hide,
                no_update, no_update, no_update, no_update, no_update,
            )
        if pathname == "/about":
            return (
                new_home, _hide,
                no_update, _hide,
                new_about, _show,
                no_update, _hide,
                no_update, _hide,
                no_update, no_update, no_update, no_update, no_update,
            )
        if pathname == "/model":
            return (
                new_home, _hide,
                no_update, _hide,
                new_about, _hide,
                no_update, _hide,
                model.layout(lang), _show,
                no_update, no_update, no_update, no_update, no_update,
            )
        # default: "/"
        return (
            new_home, _show,
            no_update, _hide,
            new_about, _hide,
            no_update, _hide,
            no_update, _hide,
            no_update, no_update, no_update, no_update, no_update,
        )

    # ── CB1: Generate scene (calls backend API) ────────────────────────
    @app.callback(
        Output("store-scene", "data"),
        Output("store-click", "data", allow_duplicate=True),
        Output("store-result", "data", allow_duplicate=True),
        Output("store-generate-click", "data"),
        Input("btn-generate", "n_clicks"),
        State("difficulty-radio", "value"),
        State("store-generate-click", "data"),
        prevent_initial_call=True,
    )
    def on_generate(
        n_clicks: int,
        difficulty: str,
        last_generate_click: Optional[int],
    ) -> Tuple[Dict, None, None, int]:
        """Call /api/scene to generate a new scene and reset game state."""
        last_click = int(last_generate_click or 0)
        # Prevent duplicate scene generation when callbacks re-fire without
        # an actual new button click.
        if not n_clicks or n_clicks <= last_click:
            return no_update, no_update, no_update, last_click

        resp = requests.get(
            f"{API_BASE}/api/scene",
            params={"difficulty": difficulty},
            headers={"X-Api-Key": INTERNAL_API_KEY},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json(), None, None, n_clicks

    # ── CB2: Capture user click on the scene graph ─────────────────────
    @app.callback(
        Output("store-click", "data"),
        Input("scene-graph", "clickData"),
        State("store-scene", "data"),
        State("store-result", "data"),
        prevent_initial_call=True,
    )
    def on_image_click(
        click_data: Optional[Dict],
        scene_data: Optional[Dict],
        result_data: Optional[Dict],
    ) -> Optional[Dict]:
        """Store click coordinates if the game is in the guessing phase."""
        # Ignore clicks before scene is generated or after result is shown
        if scene_data is None or result_data is not None:
            return no_update
        if not click_data or not click_data.get("points"):
            return no_update
        pt = click_data["points"][0]
        return {"x": round(float(pt["x"])), "y": round(float(pt["y"]))}

    # ── CB2b: Disable submit immediately on click (before CB3 finishes) ──
    @app.callback(
        Output("btn-submit", "disabled", allow_duplicate=True),
        Input("btn-submit", "n_clicks"),
        prevent_initial_call=True,
    )
    def disable_submit_on_click(_):
        return True

    # ── CB3: Evaluate guess + call /api/detect for YOLO inference ──────
    @app.callback(
        Output("store-result", "data"),
        Input("btn-submit", "n_clicks"),
        State("store-scene", "data"),
        State("store-click", "data"),
        prevent_initial_call=True,
    )
    def on_submit(
        _n_clicks: int,
        scene_data: Optional[Dict],
        click_data: Optional[Dict],
    ) -> Optional[Dict]:
        """Evaluate user guess locally and run YOLO inference in-process."""
        if not scene_data or not click_data:
            return no_update

        waldo_bbox: Tuple[int, int, int, int] = (  # type: ignore[assignment]
            tuple(scene_data["waldo_bbox"])
        )

        # ── User evaluation (pure geometry, no ML) ────────────────────
        user_found = point_in_bbox(
            float(click_data["x"]),
            float(click_data["y"]),
            waldo_bbox,
        )

        # ── YOLO inference in-process (avoids local HTTP round-trip) ──
        from ml.models.yolo_detector import detect_waldo

        img = _b64_to_pil(scene_data["img_b64"])
        detections = detect_waldo(img)

        yolo_bbox: Optional[List[int]] = None
        yolo_conf: Optional[float] = None
        yolo_found = False

        if detections:
            top = detections[0]
            yolo_bbox = list(top["bbox"])
            yolo_conf = round(float(top["confidence"]), 4)
            yolo_found = True

        return {
            "user_found": user_found,
            "yolo_found": yolo_found,
            "yolo_bbox": yolo_bbox,
            "yolo_conf": yolo_conf,
        }

    # ── CB4: Render figure + UI state from stores ──────────────────────
    @app.callback(
        Output("scene-graph", "figure"),
        Output("graph-card", "style"),
        Output("graph-placeholder", "style"),
        Output("result-panel", "children"),
        Output("btn-submit", "disabled"),
        Output("status-text", "children"),
        Input("store-scene", "data"),
        Input("store-click", "data"),
        Input("store-result", "data"),
        Input("store-game-nav", "data"),
        State("lang-store", "data"),
    )
    def render(
        scene_data: Optional[Dict],
        click_data: Optional[Dict],
        result_data: Optional[Dict],
        _nav,
        lang,
    ):
        """Single renderer: updates figure + UI based on current game state."""
        lang = lang or "pt"
        s = get_strings(lang)

        _show = {"display": "block"}
        _hide = {"display": "none"}
        _placeholder_style = {
            "height": "640px",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "center",
            "backgroundColor": _SURFACE,
            "border": f"1px solid {_T['border']}",
            "borderRadius": "10px",
            "textAlign": "center",
            "padding": "24px",
        }

        # ── No scene yet ─────────────────────────────────────────────
        if not scene_data:
            return (
                go.Figure(),
                _hide,
                _placeholder_style,
                [],
                True,
                t(s, "game.status.idle"),
            )

        img = _b64_to_pil(scene_data["img_b64"])
        waldo_bbox: Tuple[int, int, int, int] = (  # type: ignore[assignment]
            tuple(scene_data["waldo_bbox"])
        )
        difficulty = scene_data.get("difficulty", "medium")

        diff_key = {
            "easy": "game.diff.easy",
            "medium": "game.diff.medium",
            "hard": "game.diff.hard",
        }
        diff_label = t(s, diff_key.get(difficulty, "game.diff.medium"))

        # ── Result phase (after submission) ───────────────────────────
        if result_data is not None:
            yolo_bbox = (
                tuple(result_data["yolo_bbox"])
                if result_data.get("yolo_bbox")
                else None
            )
            fig = _scene_figure(
                img,
                click=click_data,
                waldo_bbox=waldo_bbox,
                yolo_bbox=yolo_bbox,  # type: ignore[arg-type]
                show_truth=True,
            )
            result_panel = _build_result_panel(result_data, lang)
            status = t(s, "game.status.done", diff=diff_label)
            return fig, _show, _hide, result_panel, True, status

        # ── Click captured — ready to submit ─────────────────────────
        if click_data:
            fig = _scene_figure(img, click=click_data)
            status = t(s, "game.status.guessed", diff=diff_label,
                       x=click_data["x"], y=click_data["y"])
            return fig, _show, _hide, [], False, status

        # ── Scene generated — waiting for user click ──────────────────
        fig = _scene_figure(img)
        status = t(s, "game.status.waiting", diff=diff_label)
        return fig, _show, _hide, [], True, status

    # ── Lang: toggle PT/EN buttons ─────────────────────────────────
    from dash import ctx as _ctx

    @app.callback(
        Output("lang-store", "data"),
        Input("lang-pt-btn", "n_clicks"),
        Input("lang-en-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_lang(_pt, _en):
        return "en" if _ctx.triggered_id == "lang-en-btn" else "pt"

    @app.callback(
        Output("lang-pt-btn", "className"),
        Output("lang-en-btn", "className"),
        Input("lang-store", "data"),
    )
    def update_lang_buttons(lang):
        if lang == "en":
            return "lang-btn", "lang-btn lang-btn-active"
        return "lang-btn lang-btn-active", "lang-btn"

    # ── Lang: translate nav chrome ──────────────────────────────────
    @app.callback(
        Output("nav-logo-text", "children"),
        Output("nav-link-home", "children"),
        Output("nav-link-game", "children"),
        Output("nav-link-competition", "children"),
        Output("nav-link-model", "children"),
        Output("nav-link-about", "children"),
        Output("footer-text", "children"),
        Input("lang-store", "data"),
    )
    def translate_nav(lang):
        s = get_strings(lang or "pt")
        return (
            t(s, "nav.title"),
            t(s, "nav.home"),
            t(s, "nav.game"),
            t(s, "comp.nav"),
            t(s, "nav.model"),
            t(s, "nav.about"),
            t(s, "footer.text"),
        )

    # ── Lang: re-render all pages on language change ────────────────
    @app.callback(
        Output("page-home", "children", allow_duplicate=True),
        Output("page-game", "children", allow_duplicate=True),
        Output("page-about", "children", allow_duplicate=True),
        Output("page-competition", "children", allow_duplicate=True),
        Output("page-model", "children", allow_duplicate=True),
        Output("store-scene", "data", allow_duplicate=True),
        Output("store-click", "data", allow_duplicate=True),
        Output("store-result", "data", allow_duplicate=True),
        Output("store-generate-click", "data", allow_duplicate=True),
        Output("store-game-nav", "data", allow_duplicate=True),
        Input("lang-store", "data"),
        State("store-game-nav", "data"),
        prevent_initial_call=True,
    )
    def on_lang_change(lang, nav_count):
        lang = lang or "pt"
        nav = (nav_count or 0) + 1
        return (
            home.layout(lang),
            game.layout(lang),
            about.layout(lang),
            no_update,          # competition: don't reset mid-game on lang change
            no_update,          # model: don't reset
            None, None, None, 0, nav,
        )

    # (model page routing handled by main route CB0)
