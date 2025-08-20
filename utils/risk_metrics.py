import numpy as np
import pandas as pd

def sharpe(returns: pd.Series, risk_free: float = 0.0, periods_per_year: int = 252) -> float:
    excess = returns - risk_free / periods_per_year
    mu = excess.mean() * periods_per_year
    sigma = excess.std() * (periods_per_year ** 0.5)
    return float(mu / (sigma + 1e-12))

def sortino(returns: pd.Series, risk_free: float = 0.0, periods_per_year: int = 252) -> float:
    excess = returns - risk_free / periods_per_year
    downside = excess[excess < 0]
    dr = downside.std() * (periods_per_year ** 0.5)
    mu = excess.mean() * periods_per_year
    return float(mu / (dr + 1e-12))

def max_drawdown(equity: pd.Series) -> float:
    roll_max = equity.cummax()
    dd = equity / roll_max - 1.0
    return float(dd.min())

def calmar(returns: pd.Series, equity: pd.Series, periods_per_year: int = 252) -> float:
    mdd = abs(max_drawdown(equity)) + 1e-12
    cagr = (1 + returns.mean()) ** periods_per_year - 1
    return float(cagr / mdd)

def cagr(equity: pd.Series, periods_per_year: int = 252) -> float:
    total_return = equity.iloc[-1] / equity.iloc[0] - 1.0
    years = len(equity) / periods_per_year
    return float((1 + total_return) ** (1 / years) - 1) if years > 0 else 0.0
