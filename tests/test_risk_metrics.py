import pandas as pd
import numpy as np
from utils.risk_metrics import sharpe, sortino, max_drawdown, cagr

def test_risk_metrics_basic():
    eq = pd.Series((1 + np.random.normal(0.0005, 0.01, size=300)).cumprod() * 100_000)
    rets = eq.pct_change().dropna()
    assert isinstance(sharpe(rets), float)
    assert isinstance(sortino(rets), float)
    assert isinstance(max_drawdown(eq), float)
    assert isinstance(cagr(eq), float)
