import pandas as pd

# ESTRATEGIA SMA (cruce)

def estrategia_sma_simple(df):
    df = df.copy()

    df["signal"] = 0

    df.loc[df["SMA_20"] > df["SMA_50"], "signal"] = 1
    df.loc[df["SMA_20"] < df["SMA_50"], "signal"] = -1

    return df

# ESTRATEGIA RSI

def estrategia_rsi(df, overbought=70, oversold=30):
    df = df.copy()

    df["signal_rsi"] = 0

    df.loc[df["RSI_14"] < oversold, "signal_rsi"] = 1
    df.loc[df["RSI_14"] > overbought, "signal_rsi"] = -1

    return df

# ESTRATEGIA COMBINADA

def estrategia_combinada(df):
    df = df.copy()

    df["signal"] = 0

    # tendencia
    df.loc[df["SMA_20"] > df["SMA_50"], "signal"] = 1
    df.loc[df["SMA_20"] < df["SMA_50"], "signal"] = -1

    # RSI
    df.loc[df["RSI_14"] > 75, "signal"] = 0
    df.loc[df["RSI_14"] < 25, "signal"] = 1

    return df