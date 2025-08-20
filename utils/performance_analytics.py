import pandas as pd
from .risk_metrics import sharpe, sortino, max_drawdown, calmar, cagr

def compute_performance_report(equity: pd.Series, trades_df: pd.DataFrame) -> pd.DataFrame:
    returns = equity.pct_change().dropna()
    report = {
        "CAGR": cagr(equity),
        "Sharpe": sharpe(returns),
        "Sortino": sortino(returns),
        "MaxDrawdown": max_drawdown(equity),
        "Calmar": calmar(returns, equity),
        "WinRate(%)": (trades_df["return"] > 0).mean() * 100.0,
        "Trades": len(trades_df),
    }
    return pd.DataFrame.from_dict(report, orient="index", columns=["value"])
