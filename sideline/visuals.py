"""
Pitch rendering for the analysis templates (matplotlib / mplsoccer).
"""

import base64
import io

from mplsoccer import Pitch
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

from sideline.metrics import DANGER_CORRIDOR


def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return b64


def make_pitch(figsize=(8, 4)):
    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#111827",
        line_color="#4B5563",
    )
    fig, ax = pitch.draw(figsize=figsize)
    return pitch, fig, ax


def _render_exploit_pitch(teams_data: list) -> str:
    # Create two subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#111827")
    fig.subplots_adjust(wspace=0.08)

    for i, (ax, td) in enumerate(zip(axes, teams_data)):
        # Draw a fresh pitch for each team
        pitch = Pitch(pitch_type="statsbomb", pitch_color="#111827",
                      line_color="#4B5563", linewidth=1.0)
        pitch.draw(ax=ax)

        if not td:
            continue
            
        def_x    = td["def_line_x_u"]
        mid_x    = td["mid_line_x_u"]
        gap_m    = td["gap_m"]
        comp     = td["comp_class"]
        false_hl = td["false_hl"]
        team     = td["team"]

        # 1. Band color is now strictly tied to compactness (Space Between)
        if comp == "Gapped":
            band_color, band_alpha = "#f59e0b", 0.12
        elif comp == "Compact":
            band_color, band_alpha = "#22c55e", 0.10
        else:
            band_color, band_alpha = "#6b7280", 0.08

        # Draw full pitch height shaded band
        ax.add_patch(plt.Rectangle(
            (min(def_x, mid_x), 0), width=abs(mid_x - def_x), height=80,
            facecolor=band_color, alpha=band_alpha, zorder=1))

        # 2. Add the False High Line warning aura BEHIND the blue line
        if false_hl:
            # Thick translucent red glow
            ax.plot([def_x, def_x], [0, 80], color="#ef4444", linewidth=12.0, linestyle="-", alpha=0.25, zorder=2)
            # Warning text near the top of the line
            ax.text(def_x - 2.5, 75, "⚠ EXPOSED", color="#ef4444", fontsize=6.5, fontweight="bold", alpha=0.90, ha="right")

        # 3. Always draw the standard dashed lines on top
        ax.plot([def_x, def_x], [0, 80], color="#3b82f6", linewidth=1.8, linestyle="--", alpha=0.80, zorder=3)
        ax.plot([mid_x, mid_x], [0, 80], color="#14b8a6", linewidth=1.8, linestyle="--", alpha=0.80, zorder=3)

        # Team Title
        ax.set_title(team.upper(), color="white", fontsize=9, fontweight="bold", pad=8)
        
        # Gap label centered inside the band
        mid_band = (def_x + mid_x) / 2
        gap_label_color = band_color if comp != "Standard" else "#9ca3af"
        ax.text(mid_band, 40, f"{gap_m}m\n({comp})",
                color=gap_label_color, fontsize=7.5, ha="center", va="center", fontweight="bold", alpha=0.90)

    handles = [
        mpatches.Patch(facecolor="#3b82f6", alpha=0.8, label="Defender line"),
        mpatches.Patch(facecolor="#14b8a6", alpha=0.8, label="Midfield line"),
        mpatches.Patch(facecolor="#f59e0b", alpha=0.6, label="Gapped — space between lines"),
        mpatches.Patch(facecolor="#22c55e", alpha=0.6, label="Compact — tight structure"),
        mpatches.Patch(facecolor="#ef4444", alpha=0.6, label="False High Line Indicator"),
    ]
    
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.06))
    
    fig.tight_layout(rect=[0, 0.05, 1, 1]) 
    return fig_to_b64(fig)


def _render_danger_pitch(teams_data: list) -> str:
    """
    Team A attacks right (normal StatsBomb orientation).
    Team B coordinates are mirrored (x -> 120-x, y -> 80-y)
    so they attack left — exactly like a real match.
    Both danger zones shown on their respective ends.
    """
    pitch, fig, ax = make_pitch(figsize=(10, 5))
    fig.patch.set_facecolor("#111827")

    dc = DANGER_CORRIDOR

    # Team A danger zone — right end (normal)
    ax.add_patch(plt.Rectangle(
        (dc["x_min"], dc["y_min"]),
        width  = dc["x_max"] - dc["x_min"],
        height = dc["y_max"] - dc["y_min"],
        facecolor="#ef4444", alpha=0.08, zorder=1,
        linewidth=1.0, edgecolor="#ef4444",
    ))

    # Team B danger zone — left end (mirrored: x 0-32, y 18-62)
    ax.add_patch(plt.Rectangle(
        (0, dc["y_min"]),
        width  = 120 - dc["x_min"],   # 32u wide from left
        height = dc["y_max"] - dc["y_min"],
        facecolor="#ef4444", alpha=0.08, zorder=1,
        linewidth=1.0, edgecolor="#ef4444",
    ))

    # Centre line label
    ax.text(60, 76, "← attack direction →",
            color="#374151", fontsize=6, alpha=0.6, ha="center")

    team_colors = [
        {"all": "#4b5563", "danger": "#00e5ff"},   # team A — cyan, attacks right
        {"all": "#44403c", "danger": "#a78bfa"},   # team B — warm grey / purple, attacks left
    ]

    for i, td in enumerate(teams_data):
        if not td or td["total_prog"] == 0:
            continue
        col = team_colors[i % 2]

        x1 = list(td["all_x1"])
        y1 = list(td["all_y1"])
        x2 = list(td["all_x2"])
        y2 = list(td["all_y2"])
        dx1 = list(td["danger_x1"])
        dy1 = list(td["danger_y1"])
        dx2 = list(td["danger_x2"])
        dy2 = list(td["danger_y2"])

        # Mirror team B coordinates so they attack left
        if i == 1:
            x1  = [120 - v for v in x1]
            y1  = [80  - v for v in y1]
            x2  = [120 - v for v in x2]
            y2  = [80  - v for v in y2]
            dx1 = [120 - v for v in dx1]
            dy1 = [80  - v for v in dy1]
            dx2 = [120 - v for v in dx2]
            dy2 = [80  - v for v in dy2]

        # All progressive passes — dim
        if x1:
            pitch.arrows(
                x1, y1, x2, y2,
                width=1.2, headwidth=6, headlength=6,
                color=col["all"], ax=ax, alpha=0.30, zorder=2,
            )

        # Danger corridor arrivals — bright
        if dx1:
            pitch.arrows(
                dx1, dy1, dx2, dy2,
                width=2, headwidth=10, headlength=10,
                color=col["danger"], ax=ax, alpha=0.90, zorder=3,
            )

        # Team label
        ly = 76 if i == 0 else 4
        lx = 62 if i == 0 else 2
        ax.text(
            lx, ly,
            f"{td['team'].upper()}  —  {td['danger_pct']}% clinical  ({td['danger_count']}/{td['total_prog']})",
            color=col["danger"], fontsize=7, alpha=0.85, fontweight="bold",
        )

    # Legend
    handles = [
        mpatches.Patch(facecolor="#4b5563", alpha=0.7, label="Progressive pass (non-dangerous)"),
        mpatches.Patch(facecolor="#00e5ff", alpha=0.8, label=f"{teams_data[0]['team']} — danger arrival (attacks right →)"),
        mpatches.Patch(facecolor="#a78bfa", alpha=0.8, label=f"{teams_data[1]['team']} — danger arrival (← attacks left)" if len(teams_data) > 1 else ""),
    ]
    fig.legend(handles=[h for h in handles if h.get_label()],
               loc="lower center", ncol=3, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    return fig_to_b64(fig)


def _block_line_x(block_x_u: float) -> float:
    """
    block_x_u is the opponent's defensive-line x in the opponent's own frame
    (their goal at x=0). The pitch is drawn in the attacking team's frame,
    where that same goal is at x=120, so the line must be mirrored.
    """
    return 120.0 - block_x_u


def _render_progress_trap_pitch(teams_data: list) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#111827")
    fig.subplots_adjust(wspace=0.06)
    team_accent = ["#00e5ff", "#a78bfa"]

    for i, (ax, td) in enumerate(zip(axes, teams_data)):
        accent = team_accent[i % 2]
        pitch  = Pitch(pitch_type="statsbomb", pitch_color="#111827",
                       line_color="#4B5563", linewidth=1.0)
        pitch.draw(ax=ax)

        if not td or td["total_attempts"] == 0:
            ax.set_title(td.get("team", ""), color="white", fontsize=9, pad=6)
            continue

        for x_start, x_end, alpha in [(0,40,0.04),(40,80,0.02),(80,120,0.03)]:
            ax.add_patch(plt.Rectangle((x_start,0), width=x_end-x_start, height=80,
                         facecolor="#ffffff", alpha=alpha, zorder=1))

        zone_colors = {"Defensive Third":"#ef4444","Middle Third":"#f59e0b","Final Third":"#a78bfa"}
        stall_df = pd.DataFrame({"x": td["stall_x"], "y": td["stall_y"]})
        if not stall_df.empty:
            stall_df["zone"] = stall_df["x"].apply(
                lambda x: "Defensive Third" if x < 40 else ("Middle Third" if x < 80 else "Final Third"))
            for zone, color in zone_colors.items():
                z = stall_df[stall_df["zone"] == zone]
                if not z.empty:
                    ax.scatter(z["x"], z["y"], marker="x", s=35, color=color,
                               alpha=0.65, linewidths=1.4, zorder=3)

        block_x = _block_line_x(td["block_x_u"])
        ax.axvline(x=block_x, color="#fbbf24", linewidth=1.8, linestyle="--", alpha=0.70, zorder=4)
        ax.text(block_x-0.8, 74, f"block {td['block_depth_m']}m", ha="right",
                color="#fbbf24", fontsize=6.5, alpha=0.85, fontweight="bold")

        ax.set_title(f"{td['team']}  —  {td['stall_rate']}% stall rate  ({td['stalled_count']}/{td['total_attempts']} attempts)",
                     color=accent, fontsize=8, fontweight="bold", pad=6)

        stall_df2 = pd.DataFrame({"x": td["stall_x"]})
        if not stall_df2.empty:
            d3 = int((stall_df2["x"] < 40).sum())
            m3 = int(((stall_df2["x"] >= 40) & (stall_df2["x"] < 80)).sum())
            f3 = int((stall_df2["x"] >= 80).sum())
            ax.text(2, 4, f"Def: {d3}  |  Mid: {m3}  |  Final: {f3}",
                    color="#9ca3af", fontsize=6.5, alpha=0.70)

    handles = [
        plt.Line2D([0],[0], marker="x", color="#ef4444", markersize=7, linewidth=0, label="Stalled — Defensive Third"),
        plt.Line2D([0],[0], marker="x", color="#f59e0b", markersize=7, linewidth=0, label="Stalled — Middle Third"),
        plt.Line2D([0],[0], marker="x", color="#a78bfa", markersize=7, linewidth=0, label="Stalled — Final Third"),
        plt.Line2D([0],[0], color="#fbbf24", linewidth=1.5, linestyle="--", label="Opponent block depth"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=6.5,
               framealpha=0.20, facecolor="#111827", edgecolor="#374151",
               labelcolor="white", bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout()
    return fig_to_b64(fig)
