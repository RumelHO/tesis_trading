import pandas as pd
import numpy as np

from src.indicadores import sma, rsi, momentum
from src.estrategias import estrategia_combinada
from src.backtesting import backtest
from src.metricas import total_return, sharpe_ratio


def optimizar_estrategia(df):

    resultados = []

    # parámetros a probar
    sma_short_list = [10, 20, 30]
    sma_long_list = [50, 100]
    rsi_overbought_list = [70, 75, 80]
    rsi_oversold_list = [20, 25, 30]

    for sma_short in sma_short_list:
        for sma_long in sma_long_list:

            # evitar combinaciones inválidas
            if sma_short >= sma_long:
                continue

            for ob in rsi_overbought_list:
                for os in rsi_oversold_list:

                    df_temp = df.copy()

                    # recalcular indicadores con parámetros
                    df_temp["SMA_short"] = sma(df_temp, window=sma_short)
                    df_temp["SMA_long"] = sma(df_temp, window=sma_long)
                    df_temp["RSI"] = rsi(df_temp)

                    # señales
                    df_temp["signal"] = 0

                    # compra
                    df_temp.loc[
                        (df_temp["SMA_short"] > df_temp["SMA_long"]) &
                        (df_temp["RSI"] < os),
                        "signal"
                    ] = 1

                    # venta
                    df_temp.loc[
                        (df_temp["SMA_short"] < df_temp["SMA_long"]) &
                        (df_temp["RSI"] > ob),
                        "signal"
                    ] = -1

                    # backtest
                    df_bt = backtest(df_temp)

                    # métricas
                    ret = total_return(df_bt["equity_curve"])
                    sharpe = sharpe_ratio(df_bt["strategy_returns"])

                    resultados.append({
                        "sma_short": sma_short,
                        "sma_long": sma_long,
                        "rsi_overbought": ob,
                        "rsi_oversold": os,
                        "return": ret,
                        "sharpe": sharpe
                    })

    df_res = pd.DataFrame(resultados)

    # ordenar por sharpe
    df_res = df_res.sort_values(by="sharpe", ascending=False)

    return df_res