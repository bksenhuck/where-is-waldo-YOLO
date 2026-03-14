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
from config.settings import API_BASE

# ── Palette — single source of truth lives in layout.py ──────────────────────
from frontend.dash_app.layout import THEME as _T

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


# ── Figure builders ───────────────────────────────────────────────────────

def _empty_figure() -> go.Figure:
    """Placeholder figure shown before first scene is generated."""
    fig = go.Figure()
    fig.add_annotation(
        text="Click <b>⚡ Generate Scene</b> to start the game!",
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
                name="Your click",
                showlegend=True,
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
                    line=dict(color=_SUCCESS, width=3),
                    fillcolor="rgba(92,184,92,0.12)",
                )
            )
            annotations.append(
                dict(
                    x=x1,
                    y=max(0, y1 - 6),
                    text="<b>Ground truth</b>",
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
                    text="<b>YOLO AI</b>",
                    showarrow=False,
                    font=dict(color=_PRIMARY, size=12),
                    bgcolor="rgba(0,0,0,0.65)",
                    xanchor="right",
                    yanchor="bottom",
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
            fixedrange=False,
        ),
        yaxis=dict(
            range=[h - 0.5, -0.5],  # top-down image orientation
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            scaleanchor="x",
            fixedrange=False,
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
        dragmode="zoom",
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
            "padding": "18px",
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


def _build_result_panel(result: Dict[str, Any]) -> html.Div:
    """Render the result card after submission."""
    user_found: bool = result["user_found"]
    yolo_found: bool = result["yolo_found"]
    yolo_conf: Optional[float] = result.get("yolo_conf")

    user_msg = "Found Waldo! 🎉" if user_found else "Missed Waldo 😅"
    user_color = _SUCCESS if user_found else _DANGER

    if yolo_found and yolo_conf is not None:
        yolo_msg = f"Found Waldo! ({yolo_conf:.0%} conf)"
    elif yolo_found:
        yolo_msg = "Found Waldo!"
    else:
        yolo_msg = "Didn't find Waldo"
    yolo_color = _SUCCESS if yolo_found else _DANGER

    # Verdict
    if user_found and yolo_found:
        verdict = "Both you and the AI found Waldo! 🏆"
        verdict_color = _SUCCESS
    elif user_found:
        verdict = "You beat the AI! 🥇"
        verdict_color = _WARNING
    elif yolo_found:
        verdict = "AI wins this round! 🤖"
        verdict_color = _PRIMARY
    else:
        verdict = "Nobody found Waldo this time…"
        verdict_color = _TEXT_MUTED

    return _result_card(
        [
            html.P(
                "RESULTS",
                style={
                    "color": _TEXT_MUTED,
                    "fontSize": "11px",
                    "fontWeight": "700",
                    "textTransform": "uppercase",
                    "letterSpacing": "1px",
                    "margin": "0 0 14px 0",
                },
            ),
            _result_row(
                "🧑" if user_found else "❌",
                "You",
                user_msg,
                user_color,
            ),
            _result_row(
                "🤖" if yolo_found else "❌",
                "YOLO AI",
                yolo_msg,
                yolo_color,
            ),
            html.Hr(
                style={
                    "border": "none",
                    "borderTop": f"1px solid {_TEXT_MUTED}40",
                    "margin": "2px 0 12px 0",
                }
            ),
            html.P(
                verdict,
                style={
                    "color": verdict_color,
                    "fontSize": "14px",
                    "fontWeight": "700",
                    "margin": "0",
                    "textAlign": "center",
                },
            ),
        ]
    )


# ── Callback registration ─────────────────────────────────────────────────

def register_callbacks(app) -> None:
    """Register all Dash callbacks onto the app instance."""

    # ── CB1: Generate scene (calls backend API) ────────────────────────
    @app.callback(
        Output("store-scene", "data"),
        Output("store-click", "data", allow_duplicate=True),
        Output("store-result", "data", allow_duplicate=True),
        Input("btn-generate", "n_clicks"),
        State("difficulty-radio", "value"),
        prevent_initial_call=True,
    )
    def on_generate(
        _n_clicks: int,
        difficulty: str,
    ) -> Tuple[Dict, None, None]:
        """Call /api/scene to generate a new scene and reset game state."""
        resp = requests.get(
            f"{API_BASE}/api/scene",
            params={"difficulty": difficulty},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json(), None, None

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
        """Evaluate user guess locally; call API for YOLO inference."""
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

        # ── YOLO inference via backend API ────────────────────────────
        resp = requests.post(
            f"{API_BASE}/api/detect",
            json={"img_b64": scene_data["img_b64"]},
            timeout=60,
        )
        resp.raise_for_status()
        detections = resp.json().get("detections", [])

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
        Output("result-panel", "children"),
        Output("btn-submit", "disabled"),
        Output("status-text", "children"),
        Input("store-scene", "data"),
        Input("store-click", "data"),
        Input("store-result", "data"),
    )
    def render(
        scene_data: Optional[Dict],
        click_data: Optional[Dict],
        result_data: Optional[Dict],
    ) -> Tuple[go.Figure, list, bool, str]:
        """Single renderer: updates figure + UI based on current game state."""

        # ── No scene yet ─────────────────────────────────────────────
        if not scene_data:
            return (
                _empty_figure(),
                [],
                True,
                "Generate a scene to start playing!",
            )

        img = _b64_to_pil(scene_data["img_b64"])
        waldo_bbox: Tuple[int, int, int, int] = (  # type: ignore[assignment]
            tuple(scene_data["waldo_bbox"])
        )
        difficulty = scene_data.get("difficulty", "medium")

        diff_labels = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}

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
            result_panel = _build_result_panel(result_data)
            status = (
                f"[{diff_labels[difficulty]}] Round over! "
                "Generate a new scene to play again."
            )
            return fig, result_panel, True, status

        # ── Click captured — ready to submit ─────────────────────────
        if click_data:
            fig = _scene_figure(img, click=click_data)
            status = (
                f"[{diff_labels[difficulty]}] Guess set at "
                f"({click_data['x']}, {click_data['y']}). "
                "Click Submit when ready!"
            )
            return fig, [], False, status

        # ── Scene generated — waiting for user click ──────────────────
        fig = _scene_figure(img)
        status = (
            f"[{diff_labels[difficulty]}] Click on the image "
            "where you think Waldo is hiding!"
        )
        return fig, [], True, status
