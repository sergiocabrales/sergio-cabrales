# 1. Imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


# 2. Tema Bloomberg
def apply_bloomberg_theme():
    mpl.rcParams.update({
        "figure.facecolor": "#000000",
        "axes.facecolor":   "#000000",
        "axes.edgecolor":   "#444444",
        "axes.labelcolor":  "#FFFFFF",
        "axes.grid":        True,
        "grid.color":       "#333333",
        "grid.linewidth":   0.5,
        "axes.grid.axis":   "y",
        "text.color":       "#FFFFFF",
        "xtick.color":      "#FFFFFF",
        "ytick.color":      "#FFFFFF",
        "xtick.labelsize":  8,
        "ytick.labelsize":  8,
        "font.family":      "monospace",
        "legend.facecolor": "#111111",
        "legend.edgecolor": "#444444",
        "legend.fontsize":  8,
        "figure.dpi":       150,
    })


apply_bloomberg_theme()

# 3. Datos (boepd), orden cronológico
trimestres = ["3T2025", "4T2025", "1T2026", "2T2026", "3T2026"]
produccion = {
    "Colombia":  [26208, 25629, 25819, 25871, 25865],
    "Ecuador":   [926,   650,   0,     0,     0],
    "Brasil":    [1002,  837,   0,     0,     0],
    "Argentina": [0,     1234,  1430,  1400,  2108],
}
total = [28136, 28351, 27249, 27271, 27973]  # Total reportado
colores = {
    "Colombia":  "#FFA028",
    "Ecuador":   "#4FC3F7",
    "Brasil":    "#81C784",
    "Argentina": "#CE93D8",
}


def fmt(v):
    return f"{v:,.0f}".replace(",", ".")


# 4. Figura y ejes
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(trimestres))

# 5. Barras apiladas
bottom = np.zeros(len(trimestres))
for pais, valores in produccion.items():
    valores = np.array(valores)
    ax.bar(x, valores, bottom=bottom, width=0.6, color=colores[pais],
           label=pais, edgecolor="#000000", linewidth=0.5, zorder=3)
    for i, v in enumerate(valores):
        if v >= 900:  # Etiquetar solo segmentos legibles
            ax.text(x[i], bottom[i] + v / 2, fmt(v), ha="center", va="center",
                    fontsize=7, color="#000000", fontweight="bold")
    bottom += valores

for i, t in enumerate(total):
    ax.text(x[i], bottom[i] + 300, fmt(t), ha="center", va="bottom",
            fontsize=9, color="#FFFFFF", fontweight="bold")

# 6. Títulos, ejes, leyenda
for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)
ax.grid(axis="y", alpha=0.3, zorder=0)
ax.grid(axis="x", visible=False)
ax.set_xticks(x, trimestres)
ax.set_ylim(0, 31000)
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: fmt(v)))
ax.set_ylabel("boepd", fontsize=9)
ax.tick_params(length=0)

# 7. Título con watermark
ax.set_title("Producción trimestral por país (boepd)  |  @SergioCabrales",
             fontsize=11, color="#FFFFFF", loc="left", pad=10)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=4,
          frameon=False)

# 8. Nota
fig.text(0.01, 0.01, "Total según reporte (puede diferir de la suma por redondeo)",
         fontsize=7, color="#888888")

# 9. Salida
plt.tight_layout()
plt.savefig("produccion_trimestral_bloomberg.png", dpi=150,
            facecolor=fig.get_facecolor())
plt.show()
