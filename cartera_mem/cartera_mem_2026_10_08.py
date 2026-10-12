"""Cartera del MEM: deuda por tipo de agente y desagregación de la deuda con generadores.

Fuente: XM — Cartera del MEM, corte al 08 de octubre de 2026.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

CORTE = "08 de octubre de 2026"
TOTAL = 4.29  # billones de pesos
DEUDA_GEN = 2.57  # billones de pesos

agentes = [  # (nombre, %, color) de abajo hacia arriba
    ("Generador", 59.93, "#D9883A"),
    ("Transportador", 25.22, "#2E5C9E"),
    ("Distribuidor", 9.34, "#5B8FD3"),
    ("Comercializador", 5.49, "#7A7A7A"),
    ("XM-Mercado", 0.02, "#B0B0B0"),
]
generacion = [
    ("Térmica", 70.01, "#B45F24"),
    ("MIX (Térmica + otra tec.)", 27.55, "#D9883A"),
    ("Solar", 1.22, "#F2C14E"),
    ("Generadores no activos", 1.11, "#9E9E9E"),
    ("Hidráulica", 0.11, "#6BAED6"),
]

UMBRAL = 8.0  # % mínimo para rotular dentro de la barra
X1, X2, W = 0.0, 1.0, 0.5

fig, ax = plt.subplots(figsize=(16, 8.5))


def apilar(x, datos, total, lado):
    base, externos = 0.0, []
    for nombre, pct, color in datos:
        val = total * pct / 100
        ax.bar(x, val, W, bottom=base, color=color, edgecolor="white", linewidth=1.2)
        ymid = base + val / 2
        if pct >= UMBRAL:
            if lado == "der" or pct < 12:
                txt = f"{nombre}\n{pct:.2f}%   ${val:.2f} B"
            else:
                txt = f"{nombre}\n{pct:.2f}%\n${val:.2f} B"
            ax.text(x, ymid, txt, ha="center", va="center", color="white",
                    fontsize=12, fontweight="bold")
        else:
            externos.append((nombre, pct, val, ymid))
        base += val
    return sorted(externos, key=lambda e: -e[3])  # evita cruce de líneas guía


ext_izq = apilar(X1, agentes, TOTAL, "izq")
ext_der = apilar(X2, generacion, DEUDA_GEN, "der")

# Rótulos externos con líneas guía
for i, (nombre, pct, val, ymid) in enumerate(ext_izq):
    ytxt = 3.45 - i * 0.30
    ax.annotate(f"{nombre}: {pct:.2f}%  (${val:.3f} B)", xy=(X1 - W / 2, ymid),
                xytext=(X1 - W / 2 - 0.12, ytxt), ha="right", va="center", fontsize=11,
                arrowprops=dict(arrowstyle="-", color="#999999", lw=0.8))
for i, (nombre, pct, val, ymid) in enumerate(ext_der):
    ytxt = 3.45 - i * 0.30
    ax.annotate(f"{nombre}: {pct:.2f}%  (${val:.3f} B)", xy=(X2 + W / 2, ymid),
                xytext=(X2 + W / 2 + 0.06, ytxt), ha="left", va="center", fontsize=11,
                arrowprops=dict(arrowstyle="-", color="#999999", lw=0.8))

# Totales
ax.text(X1, TOTAL + 0.08, f"${TOTAL:.2f} B", ha="center", va="bottom",
        fontsize=17, fontweight="bold", color="#222222")
ax.text(X2, DEUDA_GEN + 0.08, f"${DEUDA_GEN:.2f} B", ha="center", va="bottom",
        fontsize=17, fontweight="bold", color="#B45F24")

# Conector entre barras
gen_val = TOTAL * agentes[0][1] / 100
ax.add_patch(Polygon([(X1 + W / 2, 0), (X1 + W / 2, gen_val),
                      (X2 - W / 2, DEUDA_GEN), (X2 - W / 2, 0)],
                     closed=True, facecolor="#F7E4D3", alpha=0.7, edgecolor="none"))
ax.text((X1 + X2) / 2, gen_val / 2,
        f"Deuda con generadores\n${DEUDA_GEN:.2f} billones\n({agentes[0][1]:.2f}% del total)",
        ha="center", va="center", fontsize=13.5, fontweight="bold", color="#C26A1F")

# Ejes y estilo
ax.set_xlim(-1.05, 2.05)
ax.set_ylim(0, 4.6)
ax.set_xticks([X1, X2])
ax.set_xticklabels(["Deuda total del MEM\npor tipo de agente",
                    "Deuda con generadores\npor tipo de generación"],
                   fontsize=13.5, fontweight="bold")
ax.set_ylabel("Billones de pesos", fontsize=12)
ax.yaxis.grid(True, color="#EEEEEE")
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.suptitle("Cartera del MEM: deuda por tipo de agente y desagregación de la deuda con "
             "generadores  |  @SergioCabrales", x=0.05, ha="left", fontsize=16, y=0.98)
fig.text(0.05, 0.915, f"Corte al {CORTE} — billones de pesos corrientes",
         fontsize=12, color="#777777")
fig.text(0.01, 0.01, "Fuente: XM — Cartera del MEM.  Generadores no activos: agentes de "
         "generación retirados del MEM o con activos sin declaración de Operación Comercial.",
         fontsize=9, color="#999999")

fig.tight_layout(rect=(0, 0.03, 1, 0.90))
fig.savefig("cartera_mem/cartera_mem_2026_10_08.png", dpi=150)
