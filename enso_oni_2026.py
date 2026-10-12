"""Evidencia de condiciones El Niño en 2026 a partir del ONI (ERSST.v6, NOAA/CPC).

Criterio NOAA: El Niño cuando el ONI >= +0.5 °C durante al menos
5 trimestres móviles consecutivos.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def apply_eia_theme():
    mpl.rcParams.update({
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#BDBDBD",
        "axes.labelcolor": "#1A1A1A",
        "axes.grid": True,
        "grid.color": "#E0E0E0",
        "grid.linewidth": 0.7,
        "axes.grid.axis": "y",
        "text.color": "#1A1A1A",
        "xtick.color": "#1A1A1A",
        "ytick.color": "#1A1A1A",
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "font.family": "sans-serif",
        "legend.facecolor": "#FFFFFF",
        "legend.edgecolor": "#BDBDBD",
        "legend.fontsize": 8,
        "figure.dpi": 150,
    })


EIA = {
    "fg": "#1A1A1A", "blue1": "#1F5FA6", "blue2": "#4A90D9",
    "orange": "#E8821A", "red": "#C62828", "gray": "#757575",
    "watermark": "#9E9E9E",
}

apply_eia_theme()

# --- Datos: ONI (°C), NOAA/CPC ERSST.v6, actualizado 8-oct-2026 ---
SEASONS = ["DEF", "EFM", "FMA", "MAM", "AMJ", "MJJ",
           "JJA", "JAS", "ASO", "SON", "OND", "NDE"]
ONI = {
    2015: [0.7, 0.7, 0.7, 0.9, 1.0, 1.2, 1.4, 1.7, 2.0, 2.3, 2.5, 2.6],
    2023: [-0.5, -0.3, -0.1, 0.2, 0.5, 0.7, 1.0, 1.3, 1.5, 1.7, 1.9, 2.0],
    2024: [1.8, 1.5, 1.2, 0.8, 0.4, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3, -0.4],
    2025: [-0.5, -0.2, -0.1, 0.0, 0.0, 0.0, -0.1, -0.3, -0.4, -0.6, -0.6, -0.6],
    2026: [-0.4, -0.2, 0.1, 0.5, 0.9, 1.4, 1.8, 2.2],
}

# Serie continua 2024–2026
labels, values = [], []
for yr in (2024, 2025, 2026):
    for s, v in zip(SEASONS, ONI[yr]):
        labels.append(f"{s}\n{str(yr)[2:]}" if s in ("DEF", "MJJ") else s)
        values.append(v)
values = np.array(values)
x = np.arange(len(values))


def color_for(v):
    if v >= 0.5:
        return EIA["red"]
    if v <= -0.5:
        return EIA["blue1"]
    return "#BDBDBD"


fig, (ax, ax2) = plt.subplots(
    1, 2, figsize=(14, 5.5), gridspec_kw={"width_ratios": [2.1, 1]})

# --- Panel 1: ONI 2024–2026 ---
ax.bar(x, values, color=[color_for(v) for v in values], width=0.75, zorder=2)
for y, lbl, ls in [(0.5, "Umbral El Niño (+0.5)", "--"),
                   (-0.5, "Umbral La Niña (−0.5)", "--"),
                   (1.5, "Fuerte (+1.5)", ":"),
                   (2.0, "Muy fuerte (+2.0)", ":")]:
    ax.axhline(y, color=EIA["gray"], lw=0.9, ls=ls, zorder=1)
    ax.text(13.6, y + 0.05, lbl, fontsize=7, color=EIA["gray"])
ax.axhline(0, color=EIA["fg"], lw=0.8)

# Racha de 5 trimestres consecutivos >= +0.5 (MAM–JAS 2026)
start = 24 + SEASONS.index("MAM")
end = 24 + SEASONS.index("JAS")
ax.axvspan(start - 0.5, end + 0.5, color=EIA["orange"], alpha=0.12, zorder=0)
for i in range(start, end + 1):
    ax.text(i, values[i] + 0.06, f"{values[i]:+.1f}", ha="center",
            fontsize=7.5, fontweight="bold", color=EIA["red"])
ax.annotate("5 de 5 trimestres ≥ +0.5 °C\n→ criterio El Niño cumplido",
            xy=(start + 2, 1.55), xytext=(start - 8.5, 2.0),
            fontsize=8.5, fontweight="bold", color=EIA["fg"],
            arrowprops=dict(arrowstyle="->", color=EIA["fg"], lw=0.9))

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=7)
ax.set_xlim(-0.8, len(x) - 0.2)
ax.set_ylim(-1.0, 2.6)
ax.set_ylabel("Anomalía ONI (°C)", fontsize=9)
ax.set_title("ONI 2024–2026: el Pacífico ya está en condiciones El Niño  |  @SergioCabrales",
             fontsize=11, loc="left", pad=10)

# --- Panel 2: trayectoria comparada con El Niño recientes ---
idx = np.arange(len(SEASONS))
for yr, c, lw in [(2015, EIA["gray"], 1.4), (2023, EIA["blue2"], 1.4),
                  (2026, EIA["red"], 2.4)]:
    y = ONI[yr]
    ax2.plot(idx[:len(y)], y, color=c, lw=lw, marker="o", ms=3.5,
             label=f"{yr}" + (" (en curso)" if yr == 2026 else ""))
ax2.axhline(0.5, color=EIA["gray"], lw=0.9, ls="--")
ax2.axhline(0, color=EIA["fg"], lw=0.8)
ax2.annotate("JAS-26: +2.2\nvs +1.7 (2015)\ny +1.3 (2023)",
             xy=(7, 2.2), xytext=(8.3, 0.9), fontsize=7.5, color=EIA["red"],
             arrowprops=dict(arrowstyle="->", color=EIA["red"], lw=0.8))
ax2.set_xticks(idx)
ax2.set_xticklabels(SEASONS, fontsize=7, rotation=90)
ax2.set_ylim(-1.0, 2.8)
ax2.set_title("Trayectoria vs. El Niño 2015 y 2023", fontsize=10, loc="left", pad=10)
ax2.legend(loc="upper left", frameon=False)

for a in (ax, ax2):
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
    a.spines["left"].set_color("#BDBDBD")
    a.spines["bottom"].set_color("#BDBDBD")
    a.grid(axis="x", visible=False)

fig.text(0.01, 0.01,
         "Fuente: NOAA/CPC, ONI ERSST.v6 (8-oct-2026); IDEAM. Criterio NOAA: ONI ≥ +0.5 °C "
         "en ≥5 trimestres móviles consecutivos.",
         fontsize=7, color=EIA["watermark"])
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig("enso_oni_2026.png", dpi=200, bbox_inches="tight")
