import sys
sys.path.append(r"C:\Users\Planeación\Desktop\tesis_trading")

import pandas as pd
from src.optimizacion import optimizar_estrategia

# cargar datos (usa SPY primero)
df = pd.read_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\data\raw\precios_spy.csv"
)

res = optimizar_estrategia(df)

print("\nTOP 10 COMBINACIONES:\n")
print(res.head(10))

# guardar
res = res.round(4)

res.to_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\resultados\tabla_optimizacion.csv",
    sep=";",
    index=False
)