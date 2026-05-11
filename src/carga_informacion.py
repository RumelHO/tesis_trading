import pandas as pd
import os

def load_single_file(file_path):
    
    df = pd.read_csv(file_path, sep=";")

    # Convertir fecha
    df["Date"] = pd.to_datetime(df["Date"])

    # Extraer ticker del nombre del archivo
    filename = os.path.basename(file_path)
    ticker = filename.replace("precios_", "").replace(".csv", "")

    df["Ticker"] = ticker

    return df


def load_all_data(folder_path):
    
    all_data = []

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)

            print(f"Cargando {file}...")
            df = load_single_file(file_path)
            all_data.append(df)

    # Unir todos los DataFrames
    combined_df = pd.concat(all_data, ignore_index=True)

    # Ordenar por fecha
    combined_df = combined_df.sort_values(by=["Ticker", "Date"])

    return combined_df


if __name__ == "__main__":
    folder_path = r"C:\Users\Planeación\Desktop\tesis_trading\data\raw"

    df = load_all_data(folder_path)

    print(df.head())
    print("\nResumen:")
    print(df.groupby("Ticker").size())