import sys
sys.path.append(r"C:\Users\Planeación\Desktop\tesis_trading")

import pandas as pd
from src.evaluacion import evaluar_portafolio

# cargar resultados del portafolio
df = pd.read_csv("resultados_portafolio.csv")

res = evaluar_portafolio(df)

print("\n=== EVALUACIÓN DEL PORTAFOLIO ===\n")

for k, v in res.items():
    print(f"{k}: {v}")