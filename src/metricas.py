import numpy as np

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