import pandas as pd

def evaluar_portafolio(df):

    resultados = {}

    # 🔹 promedios
    resultados["avg_return_strategy"] = df["Return_Strategy"].mean()
    resultados["avg_return_bh"] = df["Return_BH"].mean()

    resultados["avg_sharpe_strategy"] = df["Sharpe_Strategy"].mean()
    resultados["avg_sharpe_bh"] = df["Sharpe_BH"].mean()

    resultados["avg_dd_strategy"] = df["DD_Strategy"].mean()
    resultados["avg_dd_bh"] = df["DD_BH"].mean()

    resultados["avg_vol_strategy"] = df["Vol_Strategy"].mean()
    resultados["avg_vol_bh"] = df["Vol_BH"].mean()

    # 🔹 conteo de ganadores
    resultados["strategy_beats_bh"] = (df["Return_Strategy"] > df["Return_BH"]).sum()
    resultados["total_assets"] = len(df)

    # 🔹 mejores y peores
    best = df.loc[df["Return_Strategy"].idxmax()]
    worst = df.loc[df["Return_Strategy"].idxmin()]

    resultados["best_ticker"] = best["Ticker"]
    resultados["best_return"] = best["Return_Strategy"]

    resultados["worst_ticker"] = worst["Ticker"]
    resultados["worst_return"] = worst["Return_Strategy"]

    return resultados