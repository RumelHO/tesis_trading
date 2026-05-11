import pandas as pd
import numpy as np

def backtest(df, initial_capital=10000):
    df = df.copy()

    # Validación
    if "Close" not in df.columns:
        raise ValueError("Falta columna Close")
    if "signal" not in df.columns:
        raise ValueError("Falta columna signal")

    # Rendimientos del activo
    df["returns"] = np.log(df["Close"] / df["Close"].shift(1))

    # Rendimientos de la estrategia
    # shift(1) para evitar "ver el futuro"
    df["strategy_returns"] = df["signal"].shift(1) * df["returns"]

    # Capital acumulado
    df["cum_returns"] = df["returns"].cumsum()
    df["cum_strategy"] = df["strategy_returns"].cumsum()

    df["equity_curve"] = initial_capital * np.exp(df["cum_strategy"])

    return df