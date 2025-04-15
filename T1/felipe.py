import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from joypy import joyplot
from matplotlib.patches import Wedge


#Criterio 5----------------------------------------------------------------------------------------------------------
# Cargar datos
df = pd.read_csv("datos/Chileautos Chile - Cars Listings.csv")

# Filtrar Santiago
comunas_santiago = [
    "Metropolitana de Santiago", "Providencia", "Ñuñoa", "Las Condes", "La Reina", "Macul", "San Miguel",
    "La Florida", "Puente Alto", "Recoleta", "Independencia", "San Joaquín", "Maipú",
    "Pudahuel", "Estación Central", "Cerrillos", "Pedro Aguirre Cerda", "El Bosque",
    "Lo Espejo", "San Bernardo", "La Granja", "Lo Prado", "Renca", "Quinta Normal",
    "Cerro Navia", "Huechuraba", "Peñalolén", "La Cisterna", "Vitacura", "Lo Barnechea"
]
df_santiago = df[df["Comuna"].isin(comunas_santiago)].copy()

# Top 10 marcas
top_marcas = df_santiago["Marca"].value_counts().nlargest(10).index
df_filtered = df_santiago[df_santiago["Marca"].isin(top_marcas)]

# Agrupar cantidad de autos por comuna y marca
conteo = df_filtered.groupby(["Comuna", "Marca"]).size().reset_index(name="Cantidad")

# Crear todas las combinaciones comuna x marca
full = pd.DataFrame(list(itertools.product(comunas_santiago, top_marcas)), columns=["Comuna", "Marca"])
conteo_full = full.merge(conteo, on=["Comuna", "Marca"], how="left").fillna(0)

# Marcar si hay datos o no
conteo_full["Tiene_dato"] = conteo_full["Cantidad"] > 0

# Normalizar tamaño
max_cantidad = conteo_full["Cantidad"].max()
conteo_full["Tamaño"] = conteo_full["Cantidad"] / max_cantidad * 300
conteo_full.loc[conteo_full["Cantidad"] == 0, "Tamaño"] = 30  # punto pequeño si no hay

# Paleta de colores por marca
palette = dict(zip(top_marcas, sns.color_palette("tab10", n_colors=len(top_marcas))))
conteo_full["Color"] = conteo_full["Marca"].map(palette)

# Gráfico
plt.figure(figsize=(14, 8))
for marca in top_marcas:
    subset = conteo_full[conteo_full["Marca"] == marca]
    # Separar los que tienen datos de los que no
    con_datos = subset[subset["Tiene_dato"]]
    sin_datos = subset[~subset["Tiene_dato"]]

    # Dibujar puntos con datos (normales)
    plt.scatter(
        con_datos["Comuna"],
        con_datos["Marca"],
        s=con_datos["Tamaño"],
        color=con_datos["Color"],
        alpha=0.7,
        label=marca
    )

    # Dibujar puntos sin datos (claros y pequeños)
    plt.scatter(
        sin_datos["Comuna"],
        sin_datos["Marca"],
        s=sin_datos["Tamaño"],
        color=sin_datos["Color"],
        alpha=0.15  # más claro
    )

plt.xticks(rotation=90)
plt.ylabel("Marca")
plt.xlabel("Comuna")
plt.title("Distribución de autos por marca y comuna (Dot matrix plot con círculos tenues)")
plt.legend(title="Marca", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()



#Criterio 4----------------------------------------------------------------------------------------------------------

comunas_santiago = [
    "Providencia", "Ñuñoa", "Las Condes", "La Reina", "Macul", "San Miguel",
    "La Florida", "Puente Alto", "Recoleta", "Independencia", "San Joaquín", "Maipú",
    "Pudahuel", "Estación Central", "Cerrillos", "Pedro Aguirre Cerda", "El Bosque", "San Bernardo", "La Granja", "Lo Prado", "Renca", "Quinta Normal",
    "Cerro Navia", "Huechuraba", "Peñalolén", "La Cisterna", "Vitacura", "Lo Barnechea"
]

# Cargar datos
df = pd.read_csv("Chileautos Chile - Cars Listings.csv")
df = df[df["Comuna"].isin(comunas_santiago)]

# Agrupar datos
conteo = df.groupby(["Comuna", "Propietarios"]).size().unstack(fill_value=0)
conteo = conteo.reindex(index=comunas_santiago)
conteo["Total"] = conteo.sum(axis=1)

# Normalizar tamaños
max_val = conteo[["Particular", "Agencia"]].values.max()
conteo["Part_norm"] = conteo["Particular"] / max_val
conteo["Agenc_norm"] = conteo["Agencia"] / max_val

# === Gráfico ===
# === Gráfico ===
spacing = 70.0  # Incrementar el espacio vertical
y = np.arange(len(conteo)) * spacing
fig_height = len(conteo) * spacing * 0.04  # Ajustar la altura de la figura
fig, ax = plt.subplots(figsize=(10, fig_height))

for i, comuna in enumerate(conteo.index):
    yc = y[i]
    
    # NUEVAS POSICIONES más separadas horizontalmente
    x_part = 0.7
    x_agenc = 1.3

    # Pelota Agencia
    ax.scatter(x_agenc, yc, s=conteo.loc[comuna, "Agenc_norm"] * 700 + 20,
               color="#3498db", alpha=0.8, edgecolor="black", linewidth=0.3,
               label="Agencia" if i == 0 else "")
    
    # Pelota Particular
    ax.scatter(x_part, yc, s=conteo.loc[comuna, "Part_norm"] * 700 + 20,
               color="#2ecc71", alpha=0.8, edgecolor="black", linewidth=0.3,
               label="Particular" if i == 0 else "")

    # Etiqueta comuna a la izquierda
    ax.text(0.4, yc, comuna, va="center", ha="right", fontsize=9)

# Ajustes visuales
ax.set_xlim(0.2, 1.8)  # Más espacio horizontal
ax.set_ylim(-spacing, y[-1] + spacing)
ax.axis("off")

# Título más arriba
plt.suptitle("Domino Dot Chart – Comparación visual por comuna", fontsize=16, y=1.02)

ax.legend(loc="upper right")
plt.tight_layout()
plt.show()