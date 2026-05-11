import pandas as pd
import numpy as np
from src.indicadores import add_indicators
from src.estrategias import estrategia_combinada
from src.backtesting import backtest

# cargar datos
df = pd.read_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\data\raw\precios_spy.csv"
)

# pipeline
df = add_indicators(df)
df = estrategia_combinada(df)
df_bt = backtest(df)

# resultados estrategia
print("\nCAPITAL FINAL (ESTRATEGIA):")
print(df_bt["equity_curve"].iloc[-1])

# COMPARACIÓN: BUY & HOLD
df_bt["buy_hold"] = 10000 * np.exp(df_bt["returns"].cumsum())

print("\nBUY & HOLD FINAL:")
print(df_bt["buy_hold"].iloc[-1])

