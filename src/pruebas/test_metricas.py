import pandas as pd
import numpy as np

from src.indicadores import add_indicators
from src.estrategias import estrategia_combinada
from src.backtesting import backtest
from src.metricas import total_return, sharpe_ratio, max_drawdown, volatility

# cargar datos
df = pd.read_csv(
    r"C:\Users\Planeación\Desktop\tesis_trading\data\raw\precios_spy.csv"
)

# pipeline completo
df = add_indicators(df)
df = estrategia_combinada(df)
df_bt = backtest(df)

# métricas estrategia
print("\n=== ESTRATEGIA ===")
print("Total Return:", total_return(df_bt["equity_curve"]))
print("Sharpe:", sharpe_ratio(df_bt["strategy_returns"]))
print("Max Drawdown:", max_drawdown(df_bt["equity_curve"]))
print("Volatilidad:", volatility(df_bt["strategy_returns"]))

# BUY & HOLD
df_bt["buy_hold"] = 10000 * np.exp(df_bt["returns"].cumsum())

print("\n=== BUY & HOLD ===")
print("Total Return:", total_return(df_bt["buy_hold"]))
print("Sharpe:", sharpe_ratio(df_bt["returns"]))
print("Max Drawdown:", max_drawdown(df_bt["buy_hold"]))
print("Volatilidad:", volatility(df_bt["returns"]))