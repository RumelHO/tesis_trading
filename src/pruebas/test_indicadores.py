import pandas as pd
from src.indicadores import add_indicators

# cargar datos
df = pd.read_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\data\raw\precios_spy.csv"
)

print("COLUMNAS ORIGINALES:")
print(df.columns)

# aplicar indicadores
df_ind = add_indicators(df)

print("\nCOLUMNAS FINALES:")
print(df_ind.columns)

print("\nHEAD:")
print(df_ind.head())
print("\nVALIDACIÓN:")
print(df_ind[["SMA_20", "SMA_50", "RSI_14", "MOM_10"]].tail(10))