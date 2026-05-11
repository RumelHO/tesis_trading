# Tesis Trading - Estrategias Cuantitativas con Análisis Técnico

## Descripción

Este proyecto corresponde al desarrollo práctico de la tesis:

**“Evaluación del desempeño de estrategias de trading basadas en indicadores técnicos en acciones y ETF mediante backtesting en mercados bursátiles”**

El objetivo principal es evaluar el desempeño de estrategias cuantitativas construidas con indicadores técnicos clásicos aplicados a activos financieros estadounidenses, utilizando procedimientos de backtesting y métricas de rendimiento ajustadas por riesgo.

El sistema fue desarrollado en Python utilizando una arquitectura modular para automatizar el procesamiento de datos, generación de señales, simulación de estrategias y evaluación estadística.

---

# Objetivos del proyecto

- Implementar estrategias de trading basadas en análisis técnico.
- Aplicar backtesting sobre datos históricos financieros.
- Comparar estrategias contra un benchmark Buy & Hold.
- Evaluar desempeño mediante métricas financieras.
- Analizar sensibilidad y optimización de parámetros.
- Generar resultados reproducibles mediante ciencia de datos aplicada.

---

# Activos analizados

El estudio incluye acciones y ETF representativos del mercado estadounidense:

- SPY
- QQQ
- DIA
- IWM
- XLF
- XLK
- XLE
- XLV
- AAPL
- MSFT
- NVDA
- AMZN
- TSLA
- GOOGL
- META

---

# Indicadores implementados

- Medias móviles simples (SMA)
- Índice de Fuerza Relativa (RSI)
- Momentum
- Señales combinadas de tendencia y sobrecompra/sobreventa

---

# Métricas financieras utilizadas

- Rendimiento acumulado (Total Return)
- Ratio de Sharpe
- Máximo Drawdown
- Volatilidad anualizada

---

# Estructura del proyecto

```text
tesis_trading/
│
├── data/
│   └── raw/
│
├── notebooks/
│   └── exploracion.ipynb
│
├── resultados/
│
├── src/
│   ├── carga_informacion.py
│   ├── indicadores.py
│   ├── estrategias.py
│   ├── backtesting.py
│   ├── metricas.py
│   ├── optimizacion.py
│   └── evaluacion.py
│
├── main.py
└── README.md
