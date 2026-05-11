import pandas as pd
from src.indicadores import add_indicators
from src.estrategias import estrategia_combinada

# cargar datos
df = pd.read_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\data\raw\precios_spy.csv"
)

# aplicar indicadores
df = add_indicators(df)

# aplicar estrategia
df = estrategia_combinada(df)

print("COLUMNAS:")
print(df.columns)

print("\nSEÑALES:")
print(df[["Close", "SMA_20", "SMA_50", "RSI_14", "signal"]].tail(20))