import pandas as pd
import numpy as np
import os

from src.indicadores import add_indicators
from src.estrategias import estrategia_combinada
from src.backtesting import backtest
from src.metricas import total_return, sharpe_ratio, max_drawdown, volatility

# carpeta de CSV
data_path = r"C:\Users\Planeación\Desktop\tesis_trading\data\raw"

resultados = []

# recorrer todos los archivos
for file in os.listdir(data_path):

    if file.endswith(".csv"):
        ticker = file.replace("precios_", "").replace(".csv", "")

        print(f"Procesando {ticker}...")

        # cargar datos
        df = pd.read_csv(os.path.join(data_path, file))

        # pipeline
        df = add_indicators(df)
        df = estrategia_combinada(df)
        df_bt = backtest(df)

        # buy & hold
        df_bt["buy_hold"] = 10000 * np.exp(df_bt["returns"].cumsum())

        # métricas
        res = {
            "Ticker": ticker,

            "Return_Strategy": total_return(df_bt["equity_curve"]),
            "Sharpe_Strategy": sharpe_ratio(df_bt["strategy_returns"]),
            "DD_Strategy": max_drawdown(df_bt["equity_curve"]),
            "Vol_Strategy": volatility(df_bt["strategy_returns"]),

            "Return_BH": total_return(df_bt["buy_hold"]),
            "Sharpe_BH": sharpe_ratio(df_bt["returns"]),
            "DD_BH": max_drawdown(df_bt["buy_hold"]),
            "Vol_BH": volatility(df_bt["returns"]),
        }

        resultados.append(res)

# convertir a DataFrame
df_resultados = pd.DataFrame(resultados)

# ordenar por rendimiento estrategia
df_resultados = df_resultados.sort_values(by="Return_Strategy", ascending=False)

print("\nRESULTADOS FINALES:")
print(df_resultados)

# guardar CSV
df_resultados.to_csv("resultados_portafolio.csv", index=False)

print("\nArchivo guardado como resultados_portafolio.csv")