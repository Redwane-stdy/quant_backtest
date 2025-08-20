from dataclasses import dataclass
import pandas as pd

@dataclass
class BacktestResult:
    trades: pd.DataFrame
    equity: pd.Series

class BaseStrategy:
    def __init__(self, lookback: int = 20, capital: float = 100_000.0, risk_fraction: float = 0.01):
        self.lookback = lookback
        self.capital = capital
        self.risk_fraction = risk_fraction

    def run(self, df: pd.DataFrame):
        raise NotImplementedError
