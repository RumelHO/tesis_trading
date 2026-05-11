import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Módulos

from src.indicadores import add_indicators
from src.estrategias import estrategia_combinada
from src.backtesting import backtest

from src.metricas import (
    total_return,
    sharpe_ratio,
    max_drawdown,
    volatility
)

# Configuración

INPUT_FILE = r"data/raw/precios_SPY.csv"
OUTPUT_FOLDER = r"resultados"

INITIAL_CAPITAL = 10000

# crear carpeta resultados
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Carga de datos

print("Cargando datos...")

df = pd.read_csv(
    INPUT_FILE,
    sep=",",
    engine="python"
)

# Indicadores

print("Calculando indicadores...")

df = add_indicators(df)

# Estrategia

print("Generando señales...")

df = estrategia_combinada(df)

# Backtesting

print("Ejecutando backtesting...")

df_bt = backtest(df)

# Buy & Hold
df_bt["buy_hold"] = (
    INITIAL_CAPITAL *
    np.exp(df_bt["returns"].cumsum())
)

# Métricas

print("Calculando métricas...")

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

# redondear
tabla = tabla.round(4)

# guardar tabla
tabla.to_csv(
    rf"{OUTPUT_FOLDER}/tabla_metricas.csv",
    sep=";",
    index=False
)

print("\nTabla de métricas guardada.")

# Gráfica 1
# Precio histórico

plt.figure(figsize=(10,5))

plt.plot(df["Close"])

plt.title("Precio histórico SPY")
plt.xlabel("Tiempo")
plt.ylabel("Precio")
plt.grid()

plt.savefig(
    rf"{OUTPUT_FOLDER}/precio_spy.png"
)

# Gráfica 2
# Medias móviles

plt.figure(figsize=(10,5))

plt.plot(df["Close"], label="Precio")
plt.plot(df["SMA_20"], label="SMA 20")
plt.plot(df["SMA_50"], label="SMA 50")

plt.title("Precio y medias móviles")
plt.legend()
plt.grid()

plt.savefig(
    rf"{OUTPUT_FOLDER}/sma_spy.png"
)

# Gráfica 3
# Señales

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

plt.savefig(
    rf"{OUTPUT_FOLDER}/senales_spy.png"
)

# Gráfica 4
# Equity vs Buy & Hold

plt.figure(figsize=(10,5))

plt.plot(
    df_bt["equity_curve"],
    label="Estrategia"
)

plt.plot(
    df_bt["buy_hold"],
    label="Buy & Hold"
)

plt.title("Estrategia vs Buy & Hold")

plt.legend()
plt.grid()

plt.savefig(
    rf"{OUTPUT_FOLDER}/equity_vs_bh.png"
)

# Final

print("\nProceso finalizado.")
print(f"Resultados guardados en: {OUTPUT_FOLDER}")