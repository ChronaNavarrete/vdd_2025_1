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

"""
Criterio 3: Marcas según comuna.
Justificación: La distribución de marcas refleja preferencias de consumo en distintas comunas. 
Esto puede relacionarse con el poder adquisitivo o el acceso a ciertos concesionarios.
"""

# Gráfico 3: Conteo de marcas más comunes por comuna (heatmap simplificado)
top_marcas = df_santiago["Marca"].value_counts().nlargest(10).index
df_marcas = df_santiago[df_santiago["Marca"].isin(top_marcas)]

pivot_marcas = df_marcas.pivot_table(index="Comuna", columns="Marca", aggfunc="size", fill_value=0)
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_marcas, cmap="YlGnBu", annot=True, fmt="d")
plt.title("Distribución de las 10 marcas más comunes por comuna")
plt.ylabel("Comuna")
plt.xlabel("Marca")
plt.tight_layout()
plt.show()

"""
Criterio 4: Propietarios por comuna.
Justificación: La distribución de vendedores particular versus agencias por comuna permite identificar 
zonas con mayor concentración de concesionarios y zonas más asociadas a venta entre particulares.
"""

# Gráfico 4: Barras apiladas – tipo de propietario por comuna
propietarios_comuna = df_santiago.groupby(["Comuna", "Propietarios"]).size().reset_index(name="Cantidad")

pivot_propietarios = propietarios_comuna.pivot(index="Comuna", columns="Propietarios", values="Cantidad").fillna(0)

pivot_propietarios = pivot_propietarios.sort_values(by="Particular", ascending=False)  # Ordenar por número de privados

# Gráfico de barras apiladas
pivot_propietarios.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6),
    colormap="Accent"
)

plt.title("Distribución de tipo de propietario por comuna (Particular vs Agencia)")
plt.xlabel("Comuna")
plt.ylabel("Cantidad de autos")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
