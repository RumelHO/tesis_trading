import yfinance as yf
import pandas as pd
import os

def download_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

if __name__ == "__main__":
    # Activos financieros
    tickers = [
        "SPY", "QQQ", "DIA", "IWM",
        "XLF", "XLK", "XLE", "XLV",
        "AAPL", "MSFT", "NVDA", "AMZN",
        "TSLA", "GOOGL", "META"
    ]

    start_date = "2015-01-01"
    end_date = "2025-12-31"

    # Ruta
    base_path = r"C:\Users\Planeación\Desktop\tesis_trading\data\raw"
    os.makedirs(base_path, exist_ok=True)

    # Descarga
    for ticker in tickers:
        print(f"Descargando {ticker}...")

        df = download_data(ticker, start_date, end_date)

        # Limpiar columnas
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Guardar CSV
        file_path = os.path.join(base_path, f"precios_{ticker}.csv")
        df.to_csv(file_path, index=True, encoding="utf-8")

        print(f"{ticker} guardado en: {file_path}")

    print("Descarga completa de todos los activos")