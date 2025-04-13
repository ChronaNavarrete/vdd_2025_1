import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Cargar el CSV
df = pd.read_csv("Chileautos Chile - Cars Listings.csv")

# Filtrar solo Santiago
comunas_santiago = [
    "Santiago", "Providencia", "Ñuñoa", "Las Condes", "La Reina", "Macul", "San Miguel",
    "La Florida", "Puente Alto", "Recoleta", "Independencia", "San Joaquín", "Maipú",
    "Pudahuel", "Estación Central", "Cerrillos", "Pedro Aguirre Cerda", "El Bosque",
    "Lo Espejo", "San Bernardo", "La Granja", "Lo Prado", "Renca", "Quinta Normal",
    "Cerro Navia", "Huechuraba", "Peñalolén", "La Cisterna", "Vitacura", "Lo Barnechea"
]
df_santiago = df[df["Comuna"].isin(comunas_santiago)].copy()

# Limpieza básica
df_santiago = df_santiago.dropna(subset=["Transmision", "price", "Comuna", "Ano"])
df_santiago["Ano"] = pd.to_numeric(df_santiago["Ano"], errors="coerce")
df_santiago = df_santiago[df_santiago["price"] > 0]
df_santiago = df_santiago[df_santiago["Ano"] > 1950]

# Gráfico 1: Diagrama de violín – Precio por tipo de transmisión
plt.figure(figsize=(10, 6))
sns.violinplot(data=df_santiago, x="Transmision", y="price", palette="coolwarm", scale="width", cut=0)
plt.title("Distribución de precios por tipo de transmisión (Santiago)")
plt.ylabel("Precio (CLP)")
plt.xlabel("Tipo de transmisión")
plt.yscale('log')  # Por la gran dispersión
plt.tight_layout()
plt.show()

# Gráfico 2: Treemap – Edad promedio de autos por comuna
df_santiago["Edad_auto"] = 2025 - df_santiago["Ano"]
edad_comuna = df_santiago.groupby("Comuna")["Edad_auto"].mean().reset_index()

fig = px.treemap(
    edad_comuna,
    path=["Comuna"],
    values="Edad_auto",
    color="Edad_auto",
    color_continuous_scale="RdYlGn_r",
    title="Edad promedio de los autos en venta por comuna (Santiago)"
)
fig.show()