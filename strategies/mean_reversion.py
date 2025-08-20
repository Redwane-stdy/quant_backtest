import pandas as pd

from .base_strategy import BaseStrategy

class ZScoreReversion(BaseStrategy):
    """Long when z<-1, short when z>1."""
    def run(self, df: pd.DataFrame):
        price = df["Close"]
        ret = price.pct_change().fillna(0.0)
        mean = ret.rolling(self.lookback).mean()
        std = ret.rolling(self.lookback).std()
        z = (ret - mean) / (std + 1e-8)
        signal = pd.Series(0, index=price.index)
        signal[z < -1] = 1
        signal[z > 1] = -1
        strat_ret = ret * signal.shift(1).fillna(0)
        equity = (1 + strat_ret).cumprod() * self.capital
        trades = pd.DataFrame({"date": price.index, "signal": signal.values, "return": strat_ret.values})
        return trades.dropna().reset_index(drop=True), pd.Series(equity, index=price.index, name="equity")
