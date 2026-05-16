import numpy as np
from scipy.stats import ttest_ind


# RETORNO TOTAL

def total_return(equity_curve):
    equity_curve = equity_curve.dropna()
    return equity_curve.iloc[-1] / equity_curve.iloc[0] - 1


# RATIO DE SHARPE

def sharpe_ratio(returns, risk_free=0):
    excess_returns = returns - risk_free
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


# DRAWDOWN MÁXIMO

def max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()


# VOLATILIDAD ANUAL

def volatility(returns):
    return returns.std() * np.sqrt(252)


# PRUEBA T DE MEDIAS

def prueba_t(strategy_returns, benchmark_returns):

    strategy = strategy_returns.dropna()
    benchmark = benchmark_returns.dropna()

    t_stat, p_value = ttest_ind(
        strategy,
        benchmark,
        equal_var=False
    )

    resultados = {
        "media_strategy": strategy.mean(),
        "media_benchmark": benchmark.mean(),
        "std_strategy": strategy.std(),
        "std_benchmark": benchmark.std(),
        "observaciones": len(strategy),
        "t_stat": t_stat,
        "p_value": p_value
    }

    return resultados

from scipy import stats


# INTERVALOS DE CONFIANZA

def intervalo_confianza(returns, confidence=0.95):

    returns = returns.dropna()

    media = returns.mean()

    n = len(returns)

    error = stats.sem(returns)

    intervalo = stats.t.interval(
        confidence,
        n - 1,
        loc=media,
        scale=error
    )

    resultados = {
        "media": media,
        "limite_inferior": intervalo[0],
        "limite_superior": intervalo[1]
    }

    return resultados