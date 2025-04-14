import pandas as pd
from unidecode import unidecode
import matplotlib.pyplot as plt
import plotly.graph_objects as go

comunas_santiago = [
    "metropolitana de santiago", "providencia", "ñuñoa", "las condes", "la reina", "macul", "san miguel",
    "la florida", "puente alto", "recoleta", "independencia", "san joaquin", "maipu",
    "pudahuel", "estacion central", "cerrillos", "pedro aguirre cerda", "el bosque",
    "lo espejo", "san bernardo", "la granja", "lo prado", "renca", "quinta normal",
    "cerro navia", "huechuraba", "peñalolen", "la cisterna", "vitacura", "lo barnechea"
]

df = pd.read_csv('Chileautos Chile - Cars Listings.csv', sep=',')
df['Comuna'] = df['Comuna'].apply(lambda x: unidecode(x) if isinstance(x, str) else x)
df['Combustible'] = df['Combustible'].str.lower()
df['Comuna'] = df['Comuna'].str.lower()
df_santiago = df[df["Comuna"].isin(comunas_santiago)].copy()

#Primer criterio
df_comb = df_santiago[['Comuna', 'Combustible']].dropna()


df_sankey = df_comb.groupby(['Comuna', 'Combustible']).size().reset_index(name='Cantidad')


comunas = list(df_sankey['Comuna'].unique())
combustibles = list(df_sankey['Combustible'].unique())
nodos = comunas + combustibles  

source_indices = [nodos.index(comuna) for comuna in df_sankey['Comuna']]
target_indices = [nodos.index(combustible) for combustible in df_sankey['Combustible']]
values = df_sankey['Cantidad'].tolist()

fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=nodos,
        pad=15,
        thickness=20,
        color="lightblue"
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values
    )
)])

fig.update_layout(title_text="Flujo de Combustibles hacia Comunas en Santiago", font_size=12)
fig.show()

#Segundo criterio
df_santiago['Kilometraje'] = (
    df_santiago['Kilometraje']
    .astype(str)
    .str.replace(r'\D', '', regex=True)
    .astype(float)
)

km_promedio_por_comuna = (
    df_santiago.groupby('Comuna')['Kilometraje']
    .mean()
    .sort_values(ascending=False)
)

comunas = km_promedio_por_comuna.index
kms = km_promedio_por_comuna.values

plt.figure(figsize=(10, 8))
plt.hlines(y=comunas, xmin=0, xmax=kms, color="gray", alpha=0.7)
plt.plot(kms, comunas, "o", color="blue")
plt.xlabel("Kilometraje promedio")
plt.title("Kilometraje promedio por comuna (Santiago)", weight="bold")
plt.tight_layout()
plt.show()