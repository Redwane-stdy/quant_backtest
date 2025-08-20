import pandas as pd

from .base_strategy import BaseStrategy

class PairStatArb(BaseStrategy):
    """Pairs strategy on spread z-score."""
    def run_pair(self, df_a: pd.DataFrame, df_b: pd.DataFrame):
        pa = df_a["Close"].pct_change().fillna(0).cumsum()
        pb = df_b["Close"].pct_change().fillna(0).cumsum()
        spread = pa - pb
        mu = spread.rolling(self.lookback).mean()
        sigma = spread.rolling(self.lookback).std() + 1e-8
        z = (spread - mu) / sigma
        signal = pd.Series(0, index=spread.index)
        signal[z < -1] = 1
        signal[z > 1] = -1
        ret_a = df_a["Close"].pct_change().fillna(0)
        ret_b = df_b["Close"].pct_change().fillna(0)
        strat_ret = (ret_a - ret_b) * signal.shift(1).fillna(0)
        equity = (1 + strat_ret).cumprod() * self.capital
        trades = pd.DataFrame({"date": spread.index, "signal": signal.values, "return": strat_ret.values})
        return trades.dropna().reset_index(drop=True), pd.Series(equity, index=spread.index, name="equity")
