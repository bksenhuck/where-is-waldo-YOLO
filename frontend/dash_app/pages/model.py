"""Model page — Display YOLO model description and training metrics/loss graphs."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

from frontend.dash_app.layout import THEME, _card
from frontend.i18n import get_strings, t

_T = THEME

# Path to the training results CSV file
RESULTS_CSV_PATH = "E:\\projects\\folder-where-is-waldo-yolo\\where-is-waldo-YOLO\\data\\models\\training\\latest_results.csv"

_AXIS_COMMON = dict(showgrid=False, zeroline=False, fixedrange=True, showline=False)
_LAYOUT_COMMON = dict(
    template="plotly_dark",
    paper_bgcolor=_T["surface"],
    plot_bgcolor=_T["surface"],
    margin=dict(l=12, r=12, t=40, b=40),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
    font=dict(color=_T["text"]),
)
_GRAPH_CONFIG = {"staticPlot": True, "displayModeBar": False}


def layout(lang: str = "pt") -> html.Div:
    """Return the model page layout."""
    s = get_strings(lang)

    try:
        df = pd.read_csv(RESULTS_CSV_PATH)
        df.columns = df.columns.str.strip()
    except Exception as e:
        return html.Div(t(s, "model.error", e=e))

    # Rename for convenience
    df = df.rename(columns={
        "metrics/precision(B)":  "Precision",
        "metrics/recall(B)":     "Recall",
        "metrics/mAP50(B)":      "mAP50",
        "metrics/mAP50-95(B)":   "mAP50-95",
        "train/box_loss":        "train_box",
        "train/cls_loss":        "train_cls",
        "train/dfl_loss":        "train_dfl",
        "val/box_loss":          "val_box",
        "val/cls_loss":          "val_cls",
        "val/dfl_loss":          "val_dfl",
    })

    epoch = df["epoch"]

    # ── Metrics figure ──────────────────────────────────────────────────────
    metrics_fig = go.Figure()
    _metric_series = [
        ("mAP50",    t(s, "model.series.map50"),     _T["primary"],  "solid"),
        ("mAP50-95", t(s, "model.series.map5095"),   _T["success"],  "solid"),
        ("Precision", t(s, "model.series.precision"), _T["warning"], "dot"),
        ("Recall",   t(s, "model.series.recall"),    _T["danger"],   "dot"),
    ]
    for col, label, color, dash in _metric_series:
        metrics_fig.add_trace(go.Scatter(
            x=epoch, y=df[col],
            mode="lines",
            name=label,
            line=dict(width=2, color=color, dash=dash),
        ))
    metrics_fig.update_layout(
        title=dict(text=t(s, "model.metrics.title"), font=dict(size=14)),
        xaxis=dict(**_AXIS_COMMON, title=t(s, "model.epoch")),
        yaxis=dict(**_AXIS_COMMON, title=t(s, "model.metrics")),
        **_LAYOUT_COMMON,
    )

    # ── Loss figure ─────────────────────────────────────────────────────────
    loss_fig = go.Figure()
    _loss_series = [
        ("train_box", t(s, "model.series.train_box"), _T["primary"],  "solid"),
        ("train_cls", t(s, "model.series.train_cls"), _T["warning"],  "solid"),
        ("train_dfl", t(s, "model.series.train_dfl"), _T["success"],  "solid"),
        ("val_box",   t(s, "model.series.val_box"),   _T["primary"],  "dash"),
        ("val_cls",   t(s, "model.series.val_cls"),   _T["warning"],  "dash"),
        ("val_dfl",   t(s, "model.series.val_dfl"),   _T["success"],  "dash"),
    ]
    for col, label, color, dash in _loss_series:
        loss_fig.add_trace(go.Scatter(
            x=epoch, y=df[col],
            mode="lines",
            name=label,
            line=dict(width=2, color=color, dash=dash),
        ))
    loss_fig.update_layout(
        title=dict(text=t(s, "model.loss.title"), font=dict(size=14)),
        xaxis=dict(**_AXIS_COMMON, title=t(s, "model.epoch")),
        yaxis=dict(**_AXIS_COMMON, title=t(s, "model.loss")),
        **_LAYOUT_COMMON,
    )

    def _guide_row(name: str, desc: str, color: str) -> html.Div:
        return html.Div(
            [
                html.Div(
                    name,
                    style={
                        "color": color,
                        "fontSize": "13px",
                        "fontWeight": "700",
                        "whiteSpace": "nowrap",
                        "minWidth": "110px",
                        "paddingTop": "1px",
                    },
                ),
                html.Div(
                    desc,
                    style={
                        "color": _T["text_muted"],
                        "fontSize": "13px",
                        "lineHeight": "1.5",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "12px",
                "alignItems": "flex-start",
                "marginBottom": "10px",
            },
        )

    def _guide_section(heading: str, rows: list) -> html.Div:
        return html.Div(
            [
                html.Div(
                    heading,
                    style={
                        "color": _T["text"],
                        "fontSize": "12px",
                        "fontWeight": "700",
                        "textTransform": "uppercase",
                        "letterSpacing": "1px",
                        "marginBottom": "12px",
                    },
                ),
                *rows,
            ],
            style={"flex": "1", "minWidth": "0"},
        )

    eval_section = _guide_section(
        t(s, "model.guide.eval.heading"),
        [
            _guide_row(t(s, "model.series.map50"),     t(s, "model.guide.map50.desc"),     _T["primary"]),
            _guide_row(t(s, "model.series.map5095"),   t(s, "model.guide.map5095.desc"),   _T["success"]),
            _guide_row(t(s, "model.series.precision"), t(s, "model.guide.precision.desc"), _T["warning"]),
            _guide_row(t(s, "model.series.recall"),    t(s, "model.guide.recall.desc"),    _T["danger"]),
        ],
    )

    loss_section = _guide_section(
        t(s, "model.guide.loss.heading"),
        [
            _guide_row("Box Loss",  t(s, "model.guide.box.desc"),     _T["primary"]),
            _guide_row("Cls Loss",  t(s, "model.guide.cls.desc"),     _T["warning"]),
            _guide_row("DFL Loss",  t(s, "model.guide.dfl.desc"),     _T["success"]),
            _guide_row(t(s, "model.guide.trainval.name"), t(s, "model.guide.trainval.desc"), _T["text_muted"]),
        ],
    )

    guide_card = _card(
        html.Div(
            [
                html.Div(
                    t(s, "model.guide.title"),
                    style={
                        "color": _T["text"],
                        "fontSize": "14px",
                        "fontWeight": "700",
                        "marginBottom": "20px",
                        "textTransform": "uppercase",
                        "letterSpacing": "1px",
                    },
                ),
                html.Div(
                    [eval_section, loss_section],
                    style={"display": "flex", "gap": "40px", "flexWrap": "wrap"},
                ),
            ]
        ),
        extra_style={"marginTop": "16px"},
    )

    return html.Div(
        [
            # ── Description card ──────────────────────────────────────────
            _card(
                html.Div([
                    html.H2(t(s, "model.title"), style={
                        "color": _T["text"],
                        "fontSize": "20px",
                        "fontWeight": "700",
                        "marginBottom": "12px",
                    }),
                    html.P(t(s, "model.description"), style={
                        "color": _T["text_muted"],
                        "fontSize": "14px",
                        "lineHeight": "1.7",
                        "margin": "0",
                    }),
                ]),
                extra_style={"marginBottom": "16px"},
            ),

            # ── Metrics graph ─────────────────────────────────────────────
            _card(
                dcc.Graph(
                    figure=metrics_fig,
                    config=_GRAPH_CONFIG,
                    style={"height": "340px"},
                ),
                extra_style={"marginBottom": "16px", "padding": "12px"},
            ),

            # ── Loss graph ────────────────────────────────────────────────
            _card(
                dcc.Graph(
                    figure=loss_fig,
                    config=_GRAPH_CONFIG,
                    style={"height": "340px"},
                ),
                extra_style={"padding": "12px"},
            ),

            # ── Metrics guide ─────────────────────────────────────────────
            guide_card,
        ],
        style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    )
