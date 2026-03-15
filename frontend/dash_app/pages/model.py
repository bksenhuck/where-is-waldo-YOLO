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
        return html.Div(f"Erro ao carregar os dados de treinamento: {e}")

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
        ("mAP50",    _T["primary"],  "solid"),
        ("mAP50-95", _T["success"],  "solid"),
        ("Precision", _T["warning"], "dot"),
        ("Recall",   _T["danger"],   "dot"),
    ]
    for col, color, dash in _metric_series:
        metrics_fig.add_trace(go.Scatter(
            x=epoch, y=df[col],
            mode="lines",
            name=col,
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
        ("train_box", "Train Box", _T["primary"],  "solid"),
        ("train_cls", "Train Cls", _T["warning"],  "solid"),
        ("train_dfl", "Train DFL", _T["success"],  "solid"),
        ("val_box",   "Val Box",   _T["primary"],  "dash"),
        ("val_cls",   "Val Cls",   _T["warning"],  "dash"),
        ("val_dfl",   "Val DFL",   _T["success"],  "dash"),
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
        ],
        style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    )
