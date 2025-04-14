import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Cargar el CSV
df = pd.read_csv("Chileautos Chile - Cars Listings.csv")

# Filtrar solo Santiago
comunas_santiago = [
    "Metropolitana de Santiago", "Providencia", "Ñuñoa", "Las Condes", "La Reina", "Macul", "San Miguel",
    "La Florida", "Puente Alto", "Recoleta", "Independencia", "San Joaquín", "Maipú",
    "Pudahuel", "Estación Central", "Cerrillos", "Pedro Aguirre Cerda", "El Bosque",
    "Lo Espejo", "San Bernardo", "La Granja", "Lo Prado", "Renca", "Quinta Normal",
    "Cerro Navia", "Huechuraba", "Peñalolén", "La Cisterna", "Vitacura", "Lo Barnechea"
]
df_santiago = df[df["Comuna"].isin(comunas_santiago)].copy()

df_santiago.to_csv("datos_filtrados_santiago.csv", index=False)

"""Criterio 1: Precio de los autos según comuna
Justificación: El precio promedio de los autos refleja diferencias territoriales en el poder adquisitivo. 
Comunas con mayor ingreso concentran vehículos más caros, evidenciando patrones de consumo diferenciados.
"""

df_santiago["price_millones"] = df_santiago["price"] / 1_000_000

# Gráfico 1: Violinplot – valor de autos por comuna
plt.figure(figsize=(12, 6))
sns.violinplot(data=df_santiago, x="Comuna", y="price_millones", palette="Set3")

plt.title("Distribución de precios de autos por comuna (Santiago)")
plt.ylabel("Precio (millones CLP)")
plt.xlabel("Comuna")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()




"""
Criterio 2: Edad promedio del auto según comuna.
Justificación: Las comunas con mayor poder adquisitivo podrían tener autos más nuevos. 
Esto permite cruzar datos socioeconómicos con los hábitos de compra.
"""

# Gráfico 2: Treemap – Edad promedio de autos por comuna
df_santiago["Edad_auto"] = 2025 - df_santiago["Ano"]
edad_comuna = df_santiago.groupby("Comuna")["Edad_auto"].mean().reset_index()

# Contar la cantidad de autos por comuna
cantidad_autos_comuna = df_santiago.groupby("Comuna").size().reset_index(name="Cantidad_autos")

# Merge con el DataFrame de la edad promedio para incluir ambos valores
edad_comuna = pd.merge(edad_comuna, cantidad_autos_comuna, on="Comuna")

fig = px.treemap(
    edad_comuna,
    path=[px.Constant("Santiago"), "Comuna"],
    values="Cantidad_autos",
    color="Edad_auto",
    color_continuous_scale="RdYlGn_r",
    title="Edad promedio de autos (color) y cantidad en venta (tamaño) por comuna"
)
fig.show()
