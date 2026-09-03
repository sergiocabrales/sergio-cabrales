# Revisión de consistencia de las gráficas — GLP Colombia

Diagnóstico de por qué los totales no coincidían entre láminas y qué se corrigió
en `GLP_Colombia_08_20_2026.ipynb`.

## 1. Cada gráfica reconstruía la oferta con un subconjunto distinto

La hoja `15. Oferta nacional de GLP` tiene dos bloques que miden cosas distintas:

- **Bloque A** (filas 10-18): producción de Ecopetrol por planta.
  `Ecopetrol Nacional = Apiay + Barranca + Cartagena + Cusiana + Cupiagua + Dina + Propilco + Floreña`
  y `Ecopetrol Importado = Terminal Fluvial`.
- **Bloque B** (filas 22-28): oferta nacional total por fuente, que además del
  bloque A incluye Termoyopal, Otros Productores e Importaciones G5 / Tumaco / Plexa.

Las láminas mezclaban los dos bloques de formas diferentes:

| Lámina | Qué sumaba | Faltaba |
|---|---|---|
| Oferta mensual nacional vs. importado | Ecopetrol Nacional + Termoyopal + Otros + importaciones | — |
| Oferta mensual/anual por fuente (Campos, Barranca, Cartagena) | Campos + refinerías + Termoyopal + importaciones | **Otros Productores** |
| Oferta Ecopetrol (campos y refinerías) | Campos sin Floreña + refinerías | **Floreña**, Termoyopal, Otros, importaciones |
| Oferta nacional por fuente (bloque B) | todo | — |

Efecto: para 2017-2019, cuando `Otros Productores` valía 1.000.000 kg/mes, la
lámina "por fuente" quedaba ~1.000 ton/mes por debajo de la de "nacional vs.
importado" para exactamente el mismo mes.

Además, `Campos` significaba dos cosas distintas en el mismo cuaderno: en una
lámina incluía Floreña **y** Termoyopal; en otra excluía ambos.

**Corrección.** Una sola capa canónica construye `oferta`, con la desagregación
`Campos / Barranca / Cartagena / Termoyopal / Otros Productores / Importado`.
Todas las láminas de oferta parten de ahí, y hay `assert` que verifican que la
pila de cada gráfica reproduce `oferta['Total']`.

## 2. El año parcial se sumaba como si estuviera completo

Las láminas anuales usaban `resample("YS").sum()`. Con datos hasta mayo de 2026,
la última barra era la suma de 5 meses junto a barras de 12, lo que la hundía
sin que se tratara de una caída real. Las notas al pie decían "*2026:
enero-abril" en unas láminas y "enero-junio" en otra, ninguna coincidente con
los datos.

**Corrección.** Las láminas anuales pasan a **promedio ton/mes** por año
(`promedio_mensual_anual`), comparable aunque el año esté incompleto, y la nota
al pie se deriva de los datos (`nota_parcial`), no se escribe a mano.

## 3. Oferta y demanda desplazadas 12 meses

`datos` (declaración de producción MinEnergía) cubre **2026-01 → 2030-12** y los
escenarios UPME cubren **2025-01 → 2029-12**. Ambas series tienen 60 puntos, así
que al graficarlas por posición (`x = range(len(datos))`) no saltaba ningún
error: la demanda de enero-2025 se dibujaba sobre la barra de enero-2026, y
todas las láminas de oferta vs. demanda quedaban corridas un año completo.

También `plt.xlim(df.index[0], df.index[-1])` fijaba el eje en 0-59 sobre un
`RangeIndex`, y en una lámina se reasignaba `x = df["Fecha_str"]` a mitad de
celda, dejando los ticks en las fechas de la proyección y las etiquetas en las
de la oferta.

**Corrección.** Se construye un eje de fechas común
(`EJE = datos.index.union(escenarios.index)`, 72 meses) y ambas series se
reindexan sobre él. Los meses sin dato quedan vacíos en lugar de desalinearse.
Solo 48 meses (2026-01 → 2029-12) tienen oferta y demanda simultáneas.

## 4. Los proyectos desaparecían en el último año

Okianus y Frontera se asignaban entre `2026-01` y `2029-12`, mientras que la
serie de oferta llega a `2030-12`: el total se desplomaba en las últimas 12
barras sin razón. Ahora el horizonte de los proyectos llega al final de la serie.

## 5. Capacidad de importación graficada como si fuera volumen

Las láminas por puerto apilaban **capacidad instalada** (G4, Colgas, Plexa Port,
Puerto Bahía) sobre la producción nacional declarada, reemplazando el volumen
importado real. El total resultante no es comparable con el de las láminas de
oferta efectiva, pero el título y las etiquetas eran los mismos.

**Corrección.** La capacidad vive en un DataFrame aparte (`capacidad`), sin
mezclarse con `datos`; los títulos y las notas al pie dicen explícitamente que
son capacidad y no volumen.

## 6. Gráficas mundiales: total rotulado ≠ altura de la pila

El total impreso encima de cada barra y el denominador de los porcentajes salían
de la fila "Total" de la hoja, mientras que las barras se dibujaban con las filas
de países. Si ambas no coinciden, los porcentajes no suman 100 % y la etiqueta no
corresponde a la pila.

**Corrección.** El total rotulado es la suma de lo graficado; la fila de la hoja
se usa solo como control y avisa por consola si difiere.

## 7. Menor: `pct_importado` (%) y `pct_importada` (cociente)

Convivían dos columnas de nombre casi idéntico, una en porcentaje y otra como
razón `Importado / Nacional`, que además puede superar 1. Se dejó una sola,
en porcentaje sobre el total.

## Verificación

El cuaderno incluye una celda de verificación que comprueba, contra los propios
datos, que:

- `Ecopetrol Nacional` (bloque B) = suma de plantas (bloque A);
- `Ecopetrol Importado` = `Terminal Fluvial`;
- el total desagregado = el total por fuente;
- la pila de cada lámina de oferta = `oferta['Total']`.

Además imprime una tabla de reconciliación con el promedio ton/mes por año que
es la base común de todas las láminas.
