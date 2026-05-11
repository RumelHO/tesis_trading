import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.indicadores import add_indicators
from src.estrategias import estrategia_combinada
from src.backtesting import backtest
from src.metricas import (
    total_return,
    sharpe_ratio,
    max_drawdown,
    volatility
)

# CARGAR DATOS

df = pd.read_csv(
    r"data/raw/precios_SPY.csv",
    sep=",",
    engine="python"
)

# INDICADORES

df = add_indicators(df)

# ESTRATEGIA

df = estrategia_combinada(df)

# BACKTEST

df_bt = backtest(df)

# Buy & Hold
df_bt["buy_hold"] = 10000 * np.exp(df_bt["returns"].cumsum())

# GRÁFICA 1: PRECIO

plt.figure(figsize=(10,5))
plt.plot(df["Close"])
plt.title("Precio histórico SPY")
plt.xlabel("Tiempo")
plt.ylabel("Precio")
plt.grid()

plt.savefig("resultados/precio_spy.png")

# GRÁFICA 2: SMA

plt.figure(figsize=(10,5))

plt.plot(df["Close"], label="Precio")
plt.plot(df["SMA_20"], label="SMA 20")
plt.plot(df["SMA_50"], label="SMA 50")

plt.title("Precio y medias móviles")
plt.legend()
plt.grid()

plt.savefig("resultados/sma_spy.png")

# GRÁFICA 3: SEÑALES

plt.figure(figsize=(12,6))

plt.plot(df["Close"], label="Precio")

buy_signals = df[df["signal"] == 1]
sell_signals = df[df["signal"] == -1]

plt.scatter(
    buy_signals.index,
    buy_signals["Close"],
    marker="^",
    label="Compra"
)

plt.scatter(
    sell_signals.index,
    sell_signals["Close"],
    marker="v",
    label="Venta"
)

plt.title("Señales de trading")
plt.legend()
plt.grid()

plt.savefig("resultados/senales_spy.png")

# GRÁFICA 4: EQUITY VS BH

plt.figure(figsize=(10,5))

plt.plot(df_bt["equity_curve"], label="Estrategia")
plt.plot(df_bt["buy_hold"], label="Buy & Hold")

plt.title("Estrategia vs Buy & Hold")
plt.legend()
plt.grid()

plt.savefig("resultados/equity_vs_bh.png")

print("Gráficas guardadas en carpeta resultados/")

# TABLA DE RESULTADOS

tabla = pd.DataFrame({
    "Metrica": [
        "Return",
        "Sharpe Ratio",
        "Max Drawdown",
        "Volatilidad"
    ],

    "Estrategia": [
        total_return(df_bt["equity_curve"]),
        sharpe_ratio(df_bt["strategy_returns"]),
        max_drawdown(df_bt["equity_curve"]),
        volatility(df_bt["strategy_returns"])
    ],

    "Buy_Hold": [
        total_return(df_bt["buy_hold"]),
        sharpe_ratio(df_bt["returns"]),
        max_drawdown(df_bt["buy_hold"]),
        volatility(df_bt["returns"])
    ]
})

print("\nTABLA FINAL:")
print(tabla)

tabla.to_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\resultados\tabla_metricas.csv",
    sep=";",
    index=False
)
