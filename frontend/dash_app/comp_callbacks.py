"""Competition callbacks — 5-round hard-difficulty Waldo vs YOLO challenge."""

from __future__ import annotations

import base64
import io
from typing import Dict, List, Optional, Tuple

import plotly.graph_objects as go
from dash import Input, Output, State, ctx, html, no_update

from backend.utils.bbox_utils import point_in_bbox
from frontend.dash_app.callbacks import (
    _b64_to_pil,
    _build_result_panel,
    _scene_figure,
)
from frontend.dash_app.layout import THEME as _T
from frontend.i18n import get_strings, t

TOTAL_ROUNDS = 5
ROUND_TIMER_SECONDS = 5  # configurable countdown per round

_BG = _T["bg"]
_SURFACE = _T["surface"]
_TEXT = _T["text"]
_TEXT_MUTED = _T["text_muted"]
_PRIMARY = _T["primary"]
_SUCCESS = _T["success"]
_WARNING = _T["warning"]
_DANGER = _T["danger"]
_BORDER = _T["border"]

_show = {"display": "block"}
_hide = {"display": "none"}
_show_flex = {"display": "flex", "gap": "12px", "alignItems": "stretch"}


# ── Scene generation helper ─────────────────────────────────────────────────

def _generate_hard_scene() -> Dict:
    """Generate a hard-difficulty Waldo scene and return the packed dict."""
    from ml.data_generation.scene_generator import generate_scene

    img, waldo_bbox = generate_scene(difficulty="hard")
    w, h = img.size
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {
        "img_b64": img_b64,
        "waldo_bbox": list(waldo_bbox),
        "width": w,
        "height": h,
        "difficulty": "hard",
    }


# ── UI helpers ──────────────────────────────────────────────────────────────

def _render_header(round_num: int, user_score: int, yolo_score: int, lang: str) -> html.Div:
    """Render the round progress header + scoreboard as a single card."""
    s = get_strings(lang)

    # Progress dots (filled = completed, empty = upcoming)
    progress_dots = html.Div(
        [
            html.Span(
                "●",
                style={
                    "fontSize": "14px",
                    "color": _SUCCESS if i < round_num else _TEXT_MUTED,
                    "margin": "0 4px",
                },
            )
            for i in range(TOTAL_ROUNDS)
        ],
        style={"display": "flex", "justifyContent": "center", "marginBottom": "4px"},
    )

    round_label = html.Div(
        t(s, "comp.round.header", n=round_num, total=TOTAL_ROUNDS),
        style={
            "color": _TEXT,
            "fontSize": "18px",
            "fontWeight": "700",
            "textAlign": "center",
            "marginBottom": "12px",
        },
    )

    scores_row = html.Div(
        [
            html.Div(
                [
                    html.Span(
                        t(s, "comp.score.you"),
                        style={
                            "fontSize": "11px",
                            "color": _TEXT_MUTED,
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "1px",
                            "display": "block",
                            "marginBottom": "2px",
                        },
                    ),
                    html.Span(
                        str(user_score),
                        style={
                            "fontSize": "40px",
                            "fontWeight": "900",
                            "color": _WARNING,
                            "lineHeight": "1",
                        },
                    ),
                ],
                style={"textAlign": "center", "flex": "1"},
            ),
            html.Div(
                "×",
                style={
                    "fontSize": "22px",
                    "fontWeight": "800",
                    "color": _TEXT_MUTED,
                    "padding": "0 20px",
                    "alignSelf": "center",
                },
            ),
            html.Div(
                [
                    html.Span(
                        t(s, "comp.score.ai"),
                        style={
                            "fontSize": "11px",
                            "color": _TEXT_MUTED,
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "1px",
                            "display": "block",
                            "marginBottom": "2px",
                        },
                    ),
                    html.Span(
                        str(yolo_score),
                        style={
                            "fontSize": "40px",
                            "fontWeight": "900",
                            "color": _PRIMARY,
                            "lineHeight": "1",
                        },
                    ),
                ],
                style={"textAlign": "center", "flex": "1"},
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
        },
    )

    return html.Div(
        [progress_dots, round_label, scores_row],
        style={
            "backgroundColor": _SURFACE,
            "border": f"1px solid {_BORDER}",
            "borderRadius": "10px",
            "padding": "14px 20px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "height": "100%",
            "boxSizing": "border-box",
        },
    )


def _render_final_content(comp: Dict, lang: str) -> html.Div:
    """Render the final result screen content (scores + round history)."""
    s = get_strings(lang)
    user_score = comp.get("user_score", 0)
    yolo_score = comp.get("yolo_score", 0)
    history: List[Dict] = comp.get("history", [])

    if user_score > yolo_score:
        verdict = t(s, "comp.final.you_win")
        verdict_color = _WARNING
    elif yolo_score > user_score:
        verdict = t(s, "comp.final.ai_win")
        verdict_color = _PRIMARY
    else:
        verdict = t(s, "comp.final.draw")
        verdict_color = _SUCCESS

    history_rows = [
        html.Tr(
            [
                html.Td(
                    f"{h['round']}",
                    style={
                        "padding": "8px 16px",
                        "color": _TEXT_MUTED,
                        "fontSize": "14px",
                        "textAlign": "center",
                    },
                ),
                html.Td(
                    "✓" if h["user_found"] else "✗",
                    style={
                        "padding": "8px 16px",
                        "color": _SUCCESS if h["user_found"] else _DANGER,
                        "fontWeight": "700",
                        "fontSize": "18px",
                        "textAlign": "center",
                    },
                ),
                html.Td(
                    "✓" if h["yolo_found"] else "✗",
                    style={
                        "padding": "8px 16px",
                        "color": _SUCCESS if h["yolo_found"] else _DANGER,
                        "fontWeight": "700",
                        "fontSize": "18px",
                        "textAlign": "center",
                    },
                ),
            ]
        )
        for h in history
    ]

    def _th(label):
        return html.Th(
            label,
            style={
                "padding": "10px 16px",
                "color": _TEXT_MUTED,
                "fontSize": "11px",
                "fontWeight": "700",
                "textTransform": "uppercase",
                "letterSpacing": "1px",
                "textAlign": "center",
            },
        )

    return html.Div(
        [
            html.H2(
                t(s, "comp.final.title"),
                style={
                    "color": _TEXT,
                    "fontSize": "28px",
                    "fontWeight": "800",
                    "textAlign": "center",
                    "margin": "0 0 8px 0",
                },
            ),
            html.Div(
                verdict,
                style={
                    "fontSize": "22px",
                    "fontWeight": "700",
                    "color": verdict_color,
                    "textAlign": "center",
                    "marginBottom": "6px",
                },
            ),
            html.Div(
                t(s, "comp.final.score", user=user_score, ai=yolo_score),
                style={
                    "fontSize": "52px",
                    "fontWeight": "900",
                    "color": _TEXT,
                    "textAlign": "center",
                    "marginBottom": "32px",
                    "lineHeight": "1",
                },
            ),
            # Round-by-round history table
            html.Div(
                html.Table(
                    [
                        html.Thead(
                            html.Tr(
                                [
                                    _th(t(s, "comp.final.round_label")),
                                    _th(t(s, "comp.score.you")),
                                    _th(t(s, "comp.score.ai")),
                                ]
                            )
                        ),
                        html.Tbody(history_rows),
                    ],
                    style={
                        "width": "100%",
                        "borderCollapse": "collapse",
                        "backgroundColor": _SURFACE,
                        "border": f"1px solid {_BORDER}",
                        "borderRadius": "8px",
                        "overflow": "hidden",
                    },
                ),
                style={"maxWidth": "360px", "margin": "0 auto"},
            ),
        ],
        style={"padding": "40px 0 0 0"},
    )


def _build_result_panel_vertical(result: Dict, lang: str = "pt") -> html.Div:
    """Vertical 3-row result card for the competition side panel (20% column)."""
    s = get_strings(lang)
    user_found: bool = result["user_found"]
    yolo_found: bool = result["yolo_found"]
    yolo_conf: Optional[float] = result.get("yolo_conf")

    from frontend.dash_app.callbacks import _SUCCESS, _DANGER, _WARNING, _PRIMARY, _TEXT_MUTED, _SURFACE

    user_msg = (
        t(s, "result.you.found") if user_found else t(s, "result.you.missed")
    )
    user_color = _SUCCESS if user_found else _DANGER

    if yolo_found and yolo_conf is not None:
        yolo_msg = t(s, "result.yolo.found", conf=f"{yolo_conf:.0%}")
    elif yolo_found:
        yolo_msg = t(s, "result.yolo.found_nc")
    else:
        yolo_msg = t(s, "result.yolo.missed")
    yolo_color = _SUCCESS if yolo_found else _DANGER

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

    def _row(label: str, icon: str, message: str, color: str) -> html.Div:
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
                        "marginBottom": "8px",
                    },
                ),
                html.Div(
                    [
                        *(
                            [html.Span(icon, style={"fontSize": "20px", "fontWeight": "700",
                                                     "color": color, "marginRight": "6px"})]
                            if icon else []
                        ),
                        html.Span(
                            message,
                            style={"color": color, "fontSize": "14px",
                                   "fontWeight": "600", "lineHeight": "1.3"},
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "justifyContent": "center",
                           "flexWrap": "wrap"},
                ),
            ],
            style={
                "flex": "1",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center",
                "textAlign": "center",
                "padding": "12px 10px",
            },
        )

    def _divider() -> html.Div:
        return html.Div(style={
            "height": "1px",
            "backgroundColor": f"{_TEXT_MUTED}30",
            "width": "100%",
        })

    return html.Div(
        [
            _row(t(s, "result.col.you"),    "+" if user_found else "−", user_msg,  user_color),
            _divider(),
            _row(t(s, "result.col.yolo"),   "+" if yolo_found else "−", yolo_msg,  yolo_color),
            _divider(),
            _row(t(s, "result.col.result"), "",                         verdict,   verdict_color),
        ],
        style={
            "backgroundColor": _SURFACE,
            "border": f"1px solid {_SUCCESS}40",
            "borderRadius": "10px",
            "display": "flex",
            "flexDirection": "column",
            "width": "100%",
            "height": "100%",
            "boxSizing": "border-box",
        },
    )


def _result_panel_empty() -> html.Div:
    """Placeholder shown in the right panel while waiting for a result."""
    return html.Div(
        style={
            "backgroundColor": _SURFACE,
            "border": f"1px solid {_BORDER}",
            "borderRadius": "10px",
            "width": "100%",
            "height": "100%",
            "boxSizing": "border-box",
        },
    )


# ── Callback registration ───────────────────────────────────────────────────

def register_comp_callbacks(app) -> None:
    """Register all competition callbacks onto the Dash app."""

    # ── COMP-CB-ADVANCE: Start first round / advance to next round ─────
    @app.callback(
        Output("store-comp", "data", allow_duplicate=True),
        Output("store-comp-scene", "data", allow_duplicate=True),
        Output("store-comp-click", "data", allow_duplicate=True),
        Output("store-comp-result", "data", allow_duplicate=True),
        Input("comp-btn-start", "n_clicks"),
        Input("comp-btn-restart", "n_clicks"),
        Input("comp-btn-next", "n_clicks"),
        State("store-comp", "data"),
        prevent_initial_call=True,
    )
    def comp_advance(
        _start: int,
        _restart: int,
        _next: int,
        comp: Optional[Dict],
    ) -> Tuple:
        # Guard: ignore spurious fires when components are dynamically mounted
        if not _start and not _restart and not _next:
            return no_update, no_update, no_update, no_update

        triggered = ctx.triggered_id

        # ── Start or Restart: brand-new competition ────────────────────
        if triggered in ("comp-btn-start", "comp-btn-restart"):
            new_comp = {
                "round": 1,
                "user_score": 0,
                "yolo_score": 0,
                "history": [],
            }
            return new_comp, _generate_hard_scene(), None, None

        # ── Next round button ──────────────────────────────────────────
        if triggered == "comp-btn-next" and comp:
            current_round = comp.get("round", 1)

            if current_round >= TOTAL_ROUNDS:
                # Mark competition as finished (round = TOTAL_ROUNDS + 1)
                finished_comp = {**comp, "round": TOTAL_ROUNDS + 1}
                return finished_comp, None, None, None
            else:
                next_comp = {**comp, "round": current_round + 1}
                return next_comp, _generate_hard_scene(), None, None

        return no_update, no_update, no_update, no_update

    # ── COMP-CB2: Capture user click on the competition scene graph ────
    @app.callback(
        Output("store-comp-click", "data"),
        Input("comp-scene-graph", "clickData"),
        State("store-comp-scene", "data"),
        State("store-comp-result", "data"),
        prevent_initial_call=True,
    )
    def comp_on_click(
        click_data: Optional[Dict],
        scene_data: Optional[Dict],
        result_data: Optional[Dict],
    ) -> Optional[Dict]:
        if scene_data is None or result_data is not None:
            return no_update
        if not click_data or not click_data.get("points"):
            return no_update
        pt = click_data["points"][0]
        return {"x": round(float(pt["x"])), "y": round(float(pt["y"]))}

    # ── COMP-CB2b: Immediately disable submit to prevent double-click ──
    @app.callback(
        Output("comp-btn-submit", "disabled", allow_duplicate=True),
        Input("comp-btn-submit", "n_clicks"),
        prevent_initial_call=True,
    )
    def comp_disable_submit(_):
        return True

    # ── COMP-CB3: Evaluate guess + YOLO inference, update scores ───────
    @app.callback(
        Output("store-comp-result", "data", allow_duplicate=True),
        Output("store-comp", "data", allow_duplicate=True),
        Input("comp-btn-submit", "n_clicks"),
        State("store-comp-scene", "data"),
        State("store-comp-click", "data"),
        State("store-comp", "data"),
        prevent_initial_call=True,
    )
    def comp_on_submit(
        _n: int,
        scene_data: Optional[Dict],
        click_data: Optional[Dict],
        comp: Optional[Dict],
    ) -> Tuple:
        if not scene_data or not click_data or not comp:
            return no_update, no_update

        waldo_bbox: Tuple[int, int, int, int] = tuple(scene_data["waldo_bbox"])  # type: ignore[assignment]

        user_found = point_in_bbox(
            float(click_data["x"]),
            float(click_data["y"]),
            waldo_bbox,
        )

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

        result = {
            "user_found": user_found,
            "yolo_found": yolo_found,
            "yolo_bbox": yolo_bbox,
            "yolo_conf": yolo_conf,
        }

        # Update competition scores and history
        updated_comp = {
            **comp,
            "user_score": comp.get("user_score", 0) + (1 if user_found else 0),
            "yolo_score": comp.get("yolo_score", 0) + (1 if yolo_found else 0),
            "history": comp.get("history", []) + [
                {
                    "round": comp.get("round", 1),
                    "user_found": user_found,
                    "yolo_found": yolo_found,
                }
            ],
        }

        return result, updated_comp

    # ── COMP-CB4: Master renderer — drives all competition UI ──────────
    _action_card_show = {
        "backgroundColor": _SURFACE,
        "border": f"1px solid {_T['border']}",
        "borderRadius": "10px",
        "padding": "14px 20px",
        "width": "100%",
        "height": "100%",
        "boxSizing": "border-box",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
    }
    _action_card_hide = {"display": "none"}

    @app.callback(
        Output("comp-header", "children"),
        Output("comp-start-screen", "style"),
        Output("comp-graph-wrapper", "style"),
        Output("comp-graph-placeholder", "style"),
        Output("comp-graph-card", "style"),
        Output("comp-scene-graph", "figure"),
        Output("comp-result-panel", "children"),
        Output("comp-final-screen", "style"),
        Output("comp-final-content", "children"),
        Output("comp-btn-submit", "disabled"),
        Output("comp-btn-submit", "style"),
        Output("comp-btn-next", "children"),
        Output("comp-btn-next", "disabled"),
        Output("comp-btn-next", "style"),
        Output("comp-action-card", "style"),
        Input("store-comp", "data"),
        Input("store-comp-scene", "data"),
        Input("store-comp-click", "data"),
        Input("store-comp-result", "data"),
        State("lang-store", "data"),
    )
    def comp_render(
        comp: Optional[Dict],
        scene_data: Optional[Dict],
        click_data: Optional[Dict],
        result_data: Optional[Dict],
        lang: Optional[str],
    ) -> Tuple:
        lang = lang or "pt"
        s = get_strings(lang)

        # Shared style constants
        _placeholder_style = {
            "height": "640px",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "center",
            "backgroundColor": _SURFACE,
            "border": f"1px solid {_BORDER}",
            "borderRadius": "10px",
            "textAlign": "center",
            "padding": "24px",
        }
        _btn_submit_hide = {"display": "none", "marginRight": "12px"}
        _btn_submit_show = {"display": "inline-block", "marginRight": "12px"}
        _btn_next_hide = {"display": "none"}
        _btn_next_show = {"display": "inline-block"}

        # ── STATE: Not started (comp is None) ─────────────────────────
        if comp is None:
            return (
                [],          # comp-header: empty
                _show,       # comp-start-screen: visible
                _hide,       # comp-graph-wrapper: hidden
                _placeholder_style,
                _hide,       # comp-graph-card
                go.Figure(),
                [],          # comp-result-panel
                _hide,       # comp-final-screen
                [],          # comp-final-content
                True,        # comp-btn-submit: disabled
                _btn_submit_hide,
                t(s, "comp.btn.next"),
                True,        # comp-btn-next: disabled
                _btn_next_hide,
                _action_card_hide,
            )

        current_round = comp.get("round", 1)

        # ── STATE: Competition finished ────────────────────────────────
        if current_round > TOTAL_ROUNDS:
            final_content = _render_final_content(comp, lang)
            return (
                [],
                _hide,          # start screen hidden
                _hide,          # game area hidden
                _placeholder_style,
                _hide,
                go.Figure(),
                [],
                _show,          # final screen visible
                final_content,
                True,
                _btn_submit_hide,
                t(s, "comp.btn.next"),
                True,
                _btn_next_hide,
                _action_card_hide,
            )

        # ── STATE: Round in progress ───────────────────────────────────
        user_score = comp.get("user_score", 0)
        yolo_score = comp.get("yolo_score", 0)
        header = _render_header(current_round, user_score, yolo_score, lang)

        # Determine next-button label
        next_btn_label = (
            t(s, "comp.btn.finish")
            if current_round == TOTAL_ROUNDS
            else t(s, "comp.btn.next")
        )

        # No scene loaded yet (comp advanced but scene not arrived)
        if scene_data is None:
            return (
                header,
                _hide,
                _show_flex,          # graph wrapper: flex row
                _placeholder_style,
                _hide,
                go.Figure(),
                _result_panel_empty(),
                _hide,
                [],
                True,
                _btn_submit_hide,
                next_btn_label,
                True,
                _btn_next_hide,
                _action_card_show,
            )

        img = _b64_to_pil(scene_data["img_b64"])
        waldo_bbox: Tuple[int, int, int, int] = tuple(scene_data["waldo_bbox"])  # type: ignore[assignment]

        # ── Sub-state: Result shown (after submit) ──────────────────
        if result_data is not None:
            yolo_bbox_raw = result_data.get("yolo_bbox")
            yolo_bbox = tuple(yolo_bbox_raw) if yolo_bbox_raw else None
            fig = _scene_figure(
                img,
                click=click_data,
                waldo_bbox=waldo_bbox,
                yolo_bbox=yolo_bbox,  # type: ignore[arg-type]
                show_truth=True,
            )
            result_panel = _build_result_panel_vertical(result_data, lang)
            return (
                header,
                _hide,
                _show_flex,
                _hide,
                _show,          # graph card: visible
                fig,
                result_panel,
                _hide,
                [],
                True,           # submit: disabled (round over)
                _btn_submit_hide,
                next_btn_label,
                False,          # next: enabled
                _btn_next_show,
                _action_card_show,
            )

        # ── Sub-state: Click captured, awaiting submit ──────────────
        if click_data:
            fig = _scene_figure(img, click=click_data)
            return (
                header,
                _hide,
                _show_flex,
                _hide,
                _show,
                fig,
                _result_panel_empty(),
                _hide,
                [],
                False,          # submit: enabled
                _btn_submit_show,
                next_btn_label,
                True,           # next: disabled until submit
                _btn_next_hide,
                _action_card_show,
            )

        # ── Sub-state: Scene loaded, awaiting click ─────────────────
        fig = _scene_figure(img)
        return (
            header,
            _hide,
            _show_flex,
            _hide,
            _show,
            fig,
            _result_panel_empty(),
            _hide,
            [],
            True,           # submit: disabled until click
            _btn_submit_hide,
            next_btn_label,
            True,
            _btn_next_hide,
            _action_card_show,
        )

    # ── COMP-CB-TIMER-CTRL: Reset/enable timer on new scene ───────────
    @app.callback(
        Output("store-comp-timer", "data"),
        Output("comp-timer-interval", "disabled"),
        Input("store-comp-scene", "data"),
        Input("store-comp-result", "data"),
        Input("store-comp", "data"),
        prevent_initial_call=True,
    )
    def comp_timer_ctrl(
        scene_data: Optional[Dict],
        result_data: Optional[Dict],
        comp: Optional[Dict],
    ) -> Tuple:
        # Start timer only when scene is loaded and round is active
        if (
            scene_data is not None
            and result_data is None
            and comp is not None
            and comp.get("round", 1) <= TOTAL_ROUNDS
        ):
            return ROUND_TIMER_SECONDS, False
        # No active round or result arrived — stop timer
        return no_update, True

    # ── COMP-CB-TIMER-TICK: Decrement every second, auto-submit at 0 ──
    @app.callback(
        Output("store-comp-timer", "data", allow_duplicate=True),
        Output("comp-timer-interval", "disabled", allow_duplicate=True),
        Output("store-comp-result", "data", allow_duplicate=True),
        Output("store-comp", "data", allow_duplicate=True),
        Input("comp-timer-interval", "n_intervals"),
        State("store-comp-timer", "data"),
        State("store-comp-result", "data"),
        State("store-comp-scene", "data"),
        State("store-comp-click", "data"),
        State("store-comp", "data"),
        prevent_initial_call=True,
    )
    def comp_timer_tick(
        _n: int,
        remaining: Optional[int],
        result_data: Optional[Dict],
        scene_data: Optional[Dict],
        click_data: Optional[Dict],
        comp: Optional[Dict],
    ) -> Tuple:
        # Guard: stop if timer already resolved or round inactive
        if remaining is None or result_data is not None or scene_data is None:
            return no_update, True, no_update, no_update

        new_remaining = remaining - 1

        if new_remaining > 0:
            return new_remaining, False, no_update, no_update

        # ── Time's up: auto-submit ─────────────────────────────────
        waldo_bbox: Tuple[int, int, int, int] = (
            tuple(scene_data["waldo_bbox"])  # type: ignore[assignment]
        )

        user_found = False
        if click_data:
            user_found = point_in_bbox(
                float(click_data["x"]),
                float(click_data["y"]),
                waldo_bbox,
            )

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

        result = {
            "user_found": user_found,
            "yolo_found": yolo_found,
            "yolo_bbox": yolo_bbox,
            "yolo_conf": yolo_conf,
            "time_expired": True,
        }

        if comp:
            updated_comp = {
                **comp,
                "user_score": comp.get("user_score", 0) + (1 if user_found else 0),
                "yolo_score": comp.get("yolo_score", 0) + (1 if yolo_found else 0),
                "history": comp.get("history", []) + [
                    {
                        "round": comp.get("round", 1),
                        "user_found": user_found,
                        "yolo_found": yolo_found,
                    }
                ],
            }
        else:
            updated_comp = no_update

        return 0, True, result, updated_comp

    # ── COMP-CB-TRANSLATE: Re-render static text on language change ───
    @app.callback(
        Output("comp-start-screen", "children"),
        Output("comp-btn-restart", "children"),
        Output("comp-graph-placeholder", "children"),
        Input("lang-store", "data"),
        prevent_initial_call=True,
    )
    def translate_comp_static(lang: Optional[str]):
        from frontend.dash_app.pages.competition import _start_screen_content
        lang = lang or "pt"
        s = get_strings(lang)
        placeholder = [
            html.Div(
                t(s, "comp.placeholder.title"),
                style={
                    "fontSize": "18px",
                    "fontWeight": "600",
                    "color": _TEXT,
                    "marginBottom": "10px",
                },
            ),
        ]
        return _start_screen_content(lang), t(s, "comp.btn.play_again"), placeholder

    # ── COMP-CB-TIMER-DISPLAY: Render the timer card ──────────────────
    @app.callback(
        Output("comp-timer-display", "children"),
        Input("store-comp-timer", "data"),
        Input("store-comp", "data"),
        Input("store-comp-result", "data"),
        State("lang-store", "data"),
        prevent_initial_call=False,
    )
    def comp_timer_display(
        remaining: Optional[int],
        comp: Optional[Dict],
        result_data: Optional[Dict],
        lang: Optional[str],
    ) -> list:
        # Hidden when competition not active or round finished
        if (
            comp is None
            or comp.get("round", 1) > TOTAL_ROUNDS
            or remaining is None
        ):
            return []

        s = get_strings(lang or "pt")
        label = t(s, "comp.timer.label")

        # Choose color based on urgency
        if result_data is not None:
            color = _TEXT_MUTED
        elif remaining <= 2:
            color = _DANGER
        elif remaining <= 3:
            color = _WARNING
        else:
            color = _SUCCESS

        return [
            html.Div(
                [
                    html.Span(
                        label,
                        style={
                            "fontSize": "11px",
                            "color": _TEXT_MUTED,
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "1px",
                            "display": "block",
                            "marginBottom": "2px",
                            "textAlign": "center",
                        },
                    ),
                    html.Span(
                        str(remaining),
                        style={
                            "fontSize": "52px",
                            "fontWeight": "900",
                            "color": color,
                            "lineHeight": "1",
                            "display": "block",
                            "textAlign": "center",
                        },
                    ),
                    html.Span(
                        "s",
                        style={
                            "fontSize": "14px",
                            "color": _TEXT_MUTED,
                            "display": "block",
                            "textAlign": "center",
                            "marginTop": "2px",
                        },
                    ),
                ],
                style={
                    "backgroundColor": _SURFACE,
                    "border": f"1px solid {_BORDER}",
                    "borderRadius": "10px",
                    "padding": "14px 20px",
                    "width": "100%",
                    "height": "100%",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "boxSizing": "border-box",
                },
            )
        ]
