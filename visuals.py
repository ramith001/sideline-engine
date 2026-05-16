"""
visuals.py
Sideline.ai v0.2 — Pitch Visualisation Modules

Three modular visual layers, all plotted onto a single mplsoccer Pitch instance.
All heavy data filtering is wrapped in @st.cache_data to avoid re-computation on
every Streamlit re-render.

Modules:
    1. Tactical Polygons  — Defensive Net (blue) + Danger Zone (red) via ConvexHull
    2. Line-Breaker Laser — The 1-3 most penetrative passes, drawn as neon arrows
    3. Pressing Trap      — High-turnover blast radius circles with hotspot overlap

Dependencies:
    pip install mplsoccer scipy matplotlib streamlit pandas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from mplsoccer import Pitch
from scipy.spatial import ConvexHull
import streamlit as st


# =============================================================================
# PITCH FACTORY
# Single shared pitch instance used by all modules.
# =============================================================================

def make_pitch():
    """
    Returns a configured mplsoccer Pitch and (fig, ax) tuple.
    Uses StatsBomb pitch dimensions (120 x 80) to match our coordinate system.
    """
    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#0d1117",
        line_color="#3d4451",
        linewidth=1.2,
    )
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.patch.set_facecolor("#0d1117")
    return pitch, fig, ax


# =============================================================================
# MODULE 1: TACTICAL POLYGON (Defensive Net + Danger Zone)
# =============================================================================

def draw_tactical_polygon(
    ax,
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    color: str,
    style_kwargs: dict,
):
    """
    Draws a ConvexHull polygon around a set of (x, y) event coordinates.

    Args:
        ax           — matplotlib axis (from make_pitch())
        x_coords     — 1D array of x coordinates
        y_coords     — 1D array of y coordinates
        color        — fill and edge color string (e.g. "#4488FF")
        style_kwargs — dict of matplotlib Polygon kwargs:
                       e.g. {"alpha": 0.25, "linestyle": "--", "linewidth": 1.5}
    """
    points = np.column_stack([x_coords, y_coords])

    # Need at least 3 non-collinear points for a hull
    if len(points) < 3:
        return

    try:
        hull = ConvexHull(points)
    except Exception:
        return

    hull_points = points[hull.vertices]
    polygon = plt.Polygon(
        hull_points,
        closed=True,
        facecolor=color,
        edgecolor=color,
        **style_kwargs,
    )
    ax.add_patch(polygon)


@st.cache_data
def get_defensive_net_coords(events: pd.DataFrame, team: str) -> tuple:
    """
    Extracts average XY positions of defensive/midfield events for the given team.
    Uses Pressures, Tackles, Interceptions as proxies for team shape.

    Returns (x_coords, y_coords) as numpy arrays.
    """
    defensive_types = ["Pressure", "Tackle", "Interception", "Block"]
    df = events[
        (events["team"] == team) &
        (events["type"].isin(defensive_types))
    ].copy()
    df = df.dropna(subset=["location"])
    df["x"] = df["location"].apply(lambda l: float(l[0]))
    df["y"] = df["location"].apply(lambda l: float(l[1]))
    return df["x"].values, df["y"].values


@st.cache_data
def get_danger_zone_coords(events: pd.DataFrame, opponent: str) -> tuple:
    """
    Extracts XY coordinates of the opponent's passes and carries
    in the final third (x >= 80u) — these represent dangerous incursions
    into the defending team's territory.

    Returns (x_coords, y_coords) as numpy arrays.
    """
    final_third_types = ["Pass", "Carry"]
    df = events[
        (events["team"] == opponent) &
        (events["type"].isin(final_third_types))
    ].copy()
    df = df.dropna(subset=["location"])
    df["x"] = df["location"].apply(lambda l: float(l[0]))
    df["y"] = df["location"].apply(lambda l: float(l[1]))

    # Final third: opponent is attacking toward x=120, so x >= 80
    df = df[df["x"] >= 80]
    return df["x"].values, df["y"].values


def render_tactical_polygons(ax, events, team, opponent, show_net, show_danger):
    """
    Orchestrates Module 1. Call this from app.py.

    Args:
        ax          — matplotlib axis
        events      — full match events DataFrame
        team        — name of the team we are analysing (defending side)
        opponent    — name of the opposing team (attacking side)
        show_net    — bool from Streamlit checkbox
        show_danger — bool from Streamlit checkbox
    """
    if show_net:
        x, y = get_defensive_net_coords(events, team)
        if len(x) >= 3:
            draw_tactical_polygon(
                ax, x, y,
                color="#3a7bd5",
                style_kwargs={
                    "alpha": 0.22,
                    "linestyle": "--",
                    "linewidth": 1.8,
                },
            )

    if show_danger:
        x, y = get_danger_zone_coords(events, opponent)
        if len(x) >= 3:
            draw_tactical_polygon(
                ax, x, y,
                color="#e84560",
                style_kwargs={
                    "alpha": 0.30,
                    "linestyle": "-",
                    "linewidth": 1.5,
                },
            )


# =============================================================================
# MODULE 2: LINE-BREAKER LASER
# =============================================================================

@st.cache_data
def get_line_breaker_passes(events: pd.DataFrame, team: str, top_n: int = 3) -> pd.DataFrame:
    """
    Finds the most penetrative completed passes for a given team.

    "Penetrative" is defined as passes whose end location (x2) exceeds the
    x-coordinates of the most defenders in a single pass — i.e., the pass
    skips over the most players by X-coordinate.

    Methodology:
        For each completed pass by `team`, count how many opponent defensive
        events (Pressure, Tackle, Block) have an X coordinate between the
        pass start and end X. This approximates "defenders bypassed."

    Returns top_n rows sorted descending by defenders_bypassed.
    """
    # Completed passes for this team
    passes = events[
        (events["team"] == team) &
        (events["type"] == "Pass") &
        (events["period"] != 5)
    ].copy()
    passes = passes.dropna(subset=["location", "pass_end_location"])
    passes = passes[passes["pass_outcome"].isna()]

    passes["x1"] = passes["location"].apply(lambda l: float(l[0]))
    passes["y1"] = passes["location"].apply(lambda l: float(l[1]))
    passes["x2"] = passes["pass_end_location"].apply(lambda l: float(l[0]))
    passes["y2"] = passes["pass_end_location"].apply(lambda l: float(l[1]))

    # Only forward passes (x2 > x1)
    passes = passes[passes["x2"] > passes["x1"]].copy()

    # Opponent defensive positions
    opp_teams = events["team"].dropna().unique()
    opponent = [t for t in opp_teams if t != team]
    if not opponent:
        return pd.DataFrame()
    opponent = opponent[0]

    opp_def = events[
        (events["team"] == opponent) &
        (events["type"].isin(["Pressure", "Tackle", "Block", "Interception"]))
    ].copy()
    opp_def = opp_def.dropna(subset=["location"])
    opp_def["ox"] = opp_def["location"].apply(lambda l: float(l[0]))

    opp_x_vals = opp_def["ox"].values

    def count_bypassed(row):
        """Count opponent defenders with x between pass start and end."""
        return int(np.sum((opp_x_vals > row["x1"]) & (opp_x_vals < row["x2"])))

    passes["defenders_bypassed"] = passes.apply(count_bypassed, axis=1)
    passes = passes.sort_values("defenders_bypassed", ascending=False)
    return passes.head(top_n)


def render_line_breakers(ax, events, team):
    """
    Draws neon laser arrows for the top penetrative passes.
    The glow effect is achieved by stacking 3 arrows:
        outer (wide, low alpha) → mid → inner (thin, full color)

    Args:
        ax     — matplotlib axis
        events — full match events DataFrame
        team   — name of the attacking team
    """
    passes = get_line_breaker_passes(events, team)
    if passes.empty:
        return

    neon_color   = "#00ffe0"   # cyan-green neon
    glow_color   = "#00ffe0"

    for _, row in passes.iterrows():
        x1, y1, x2, y2 = row["x1"], row["y1"], row["x2"], row["y2"]
        n_bypassed = int(row["defenders_bypassed"])

        # Glow layers: draw from widest/most transparent to thinnest/opaque
        glow_layers = [
            {"lw": 9,   "alpha": 0.06},
            {"lw": 5,   "alpha": 0.12},
            {"lw": 2.5, "alpha": 0.90},
        ]
        for layer in glow_layers:
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=glow_color,
                    lw=layer["lw"],
                    alpha=layer["alpha"],
                    mutation_scale=18,
                ),
            )

        # Label: number of defenders bypassed
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 1.5
        ax.text(
            mid_x, mid_y,
            f"+{n_bypassed}",
            color=neon_color,
            fontsize=8,
            fontweight="bold",
            ha="center",
            va="bottom",
            alpha=0.85,
        )


# =============================================================================
# MODULE 3: PRESSING TRAP BLAST RADIUS
# =============================================================================

@st.cache_data
def get_high_turnover_locations(events: pd.DataFrame, team: str) -> pd.DataFrame:
    """
    Finds High Turnovers: moments where the team won the ball in the opponent's
    half (x >= 60) that were immediately preceded by a Pressure event.

    Methodology:
        1. Find all ball-winning events for `team` in the attacking third (x >= 60):
           Ball Recovery, Interception, Tackle (won)
        2. For each, check whether the immediately preceding event in the timeline
           was a Pressure by the same team (within 5 seconds)
        3. Return the (x, y) locations of confirmed pressing traps

    Returns DataFrame with columns: x, y, event_type, timestamp.
    """
    # Ball-winning events in attacking half
    winning_types = ["Ball Recovery", "Interception"]
    df = events[
        (events["team"] == team) &
        (events["type"].isin(winning_types))
    ].copy()
    df = df.dropna(subset=["location"])
    df["x"] = df["location"].apply(lambda l: float(l[0]))
    df["y"] = df["location"].apply(lambda l: float(l[1]))
    df = df[df["x"] >= 60].copy()   # attacking half only
    df = df.sort_values(["period", "timestamp"]).reset_index()

    # All pressure events by this team
    pressures = events[
        (events["team"] == team) &
        (events["type"] == "Pressure")
    ].copy()
    pressures = pressures.sort_values(["period", "timestamp"])

    # For each turnover, check if a pressure preceded it within 5 seconds
    trap_rows = []
    for _, win_row in df.iterrows():
        period    = win_row["period"]
        ts        = win_row["timestamp"]
        period_pressures = pressures[pressures["period"] == period]

        # Find pressures within 5 seconds before the turnover
        def ts_to_seconds(t):
            if isinstance(t, str):
                parts = t.split(":")
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
            return 0

        win_secs  = ts_to_seconds(str(ts))
        preceded  = period_pressures[
            period_pressures["timestamp"].apply(
                lambda t: abs(ts_to_seconds(str(t)) - win_secs) <= 5
            )
        ]

        if not preceded.empty:
            trap_rows.append({
                "x":          win_row["x"],
                "y":          win_row["y"],
                "event_type": win_row["type"],
                "timestamp":  ts,
            })

    return pd.DataFrame(trap_rows)


def render_pressing_trap(ax, events, team, blast_radius: float = 6.0):
    """
    Draws semi-transparent blast radius circles at high-turnover locations.
    Overlapping circles naturally darken the hotspot zones.

    Args:
        ax            — matplotlib axis
        events        — full match events DataFrame
        team          — team that executed the pressing traps
        blast_radius  — radius of each circle in pitch units (default 6u ≈ 5.25m)
    """
    traps = get_high_turnover_locations(events, team)
    if traps.empty:
        return

    for _, row in traps.iterrows():
        circle = plt.Circle(
            (row["x"], row["y"]),
            radius=blast_radius,
            facecolor="#ff6600",
            edgecolor="#ff9900",
            linewidth=1.0,
            alpha=0.22,       # low alpha = overlapping zones darken naturally
        )
        ax.add_patch(circle)

        # Small dot at exact turnover point
        ax.scatter(
            row["x"], row["y"],
            s=28,
            color="#ff9900",
            alpha=0.75,
            zorder=5,
        )


# =============================================================================
# LEGEND BUILDER
# =============================================================================

def add_visual_legend(ax, show_net, show_danger, show_laser, show_trap):
    """
    Adds a compact legend to the pitch for whichever modules are active.
    """
    handles = []
    if show_net:
        handles.append(mpatches.Patch(
            facecolor="#3a7bd5", alpha=0.5,
            label="Defensive Net",
            linestyle="--",
        ))
    if show_danger:
        handles.append(mpatches.Patch(
            facecolor="#e84560", alpha=0.5,
            label="Danger Zone",
        ))
    if show_laser:
        handles.append(mpatches.Patch(
            facecolor="#00ffe0", alpha=0.8,
            label="Line-Breaker Pass",
        ))
    if show_trap:
        handles.append(mpatches.Patch(
            facecolor="#ff6600", alpha=0.5,
            label="Pressing Trap",
        ))
    if handles:
        ax.legend(
            handles=handles,
            loc="lower left",
            fontsize=8,
            framealpha=0.3,
            facecolor="#0d1117",
            edgecolor="#3d4451",
            labelcolor="white",
        )
