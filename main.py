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
    volatility,
    prueba_t,
    intervalo_confianza
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

# PRUEBA T

resultados_t = prueba_t(
    df_bt["strategy_returns"],
    df_bt["returns"]
)

print("\nResultados prueba t:")
print(resultados_t)

# Tabla prueba t

tabla_t = pd.DataFrame({

    "Metrica": [
        "Media Estrategia",
        "Media Buy & Hold",
        "Std Estrategia",
        "Std Buy & Hold",
        "Observaciones",
        "Estadistico t",
        "p-value"
    ],

    "Valor": [
        resultados_t["media_strategy"],
        resultados_t["media_benchmark"],
        resultados_t["std_strategy"],
        resultados_t["std_benchmark"],
        resultados_t["observaciones"],
        resultados_t["t_stat"],
        resultados_t["p_value"]
    ]

})

# redondear
tabla_t = tabla_t.round(6)

# guardar csv

tabla_t.to_csv(
    rf"{OUTPUT_FOLDER}/tabla_prueba_t.csv",
    sep=";",
    index=False
)

print("\nTabla prueba t guardada.")

# INTERVALOS DE CONFIANZA

ic_strategy = intervalo_confianza(
    df_bt["strategy_returns"]
)

ic_bh = intervalo_confianza(
    df_bt["returns"]
)

# Tabla intervalos de confianza

tabla_ic = pd.DataFrame({

    "Estrategia": [
        "Estrategia cuantitativa",
        "Buy & Hold"
    ],

    "Media": [
        ic_strategy["media"],
        ic_bh["media"]
    ],

    "Limite_Inferior": [
        ic_strategy["limite_inferior"],
        ic_bh["limite_inferior"]
    ],

    "Limite_Superior": [
        ic_strategy["limite_superior"],
        ic_bh["limite_superior"]
    ]

})

# redondear

tabla_ic = tabla_ic.round(6)

# guardar csv

tabla_ic.to_csv(
    rf"{OUTPUT_FOLDER}/intervalos_confianza.csv",
    sep=";",
    index=False
)

print("\nTabla de intervalos de confianza guardada.")

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

# Gráfica 5
# Histograma de retornos

plt.figure(figsize=(10,5))

plt.hist(
    df_bt["strategy_returns"].dropna(),
    bins=50
)

plt.title("Distribución de retornos de la estrategia")
plt.xlabel("Retornos")
plt.ylabel("Frecuencia")
plt.grid()

plt.savefig(
    rf"{OUTPUT_FOLDER}/histograma_retornos.png"
)

# Gráfica 6
# Drawdown

rolling_max = df_bt["equity_curve"].cummax()

drawdown = (
    df_bt["equity_curve"] - rolling_max
) / rolling_max

plt.figure(figsize=(10,5))

plt.plot(drawdown)

plt.title("Drawdown de la estrategia")
plt.xlabel("Tiempo")
plt.ylabel("Drawdown")
plt.grid()

plt.savefig(
    rf"{OUTPUT_FOLDER}/drawdown.png"
)

# Gráfica 7
# Rolling volatility

rolling_vol = (
    df_bt["strategy_returns"]
    .rolling(30)
    .std()
    * np.sqrt(252)
)

plt.figure(figsize=(10,5))

plt.plot(rolling_vol)

plt.title("Volatilidad móvil anualizada")
plt.xlabel("Tiempo")
plt.ylabel("Volatilidad")
plt.grid()

plt.savefig(
    rf"{OUTPUT_FOLDER}/rolling_volatility.png"
)