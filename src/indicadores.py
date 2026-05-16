import pandas as pd
import numpy as np

# VALIDACIÓN DE DATOS

def _validate_df(df, price_col="Close"):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    if price_col not in df.columns:
        raise ValueError(f"No existe la columna '{price_col}' en el dataframe")

    return df

# 1. MEDIA MÓVIL SIMPLE

def sma(df, window=20, price_col="Close"):
    return df[price_col].rolling(window=window, min_periods=window).mean()

# 2. MOMENTUM

def momentum(df, window=10, price_col="Close"):
    return np.log(df[price_col] / df[price_col].shift(window))

# 3. RSI

def rsi(df, window=14, price_col="Close"):
    delta = df[price_col].diff()

    gain = delta.clip(lower=0).rolling(window=window, min_periods=window).mean()
    loss = (-delta.clip(upper=0)).rolling(window=window, min_periods=window).mean()

    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))

    return rsi

# 4. PIPELINE PRINCIPAL

def add_indicators(df):
    df = _validate_df(df)

    df["SMA_20"] = sma(df)
    df["SMA_50"] = sma(df, window=50)

    df["RSI_14"] = rsi(df)

    df["MOM_10"] = momentum(df)

    return df