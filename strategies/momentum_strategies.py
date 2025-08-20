import pandas as pd

from .base_strategy import BaseStrategy

class SimpleMomentum(BaseStrategy):
    """Long when return_{lookback} > 0, flat otherwise."""
    def run(self, df: pd.DataFrame):
        price = df["Close"]
        ret_lb = price.pct_change(self.lookback)
        signal = (ret_lb > 0).astype(int)
        daily_ret = price.pct_change().fillna(0.0)
        strat_ret = daily_ret * signal.shift(1).fillna(0)
        equity = (1 + strat_ret).cumprod() * self.capital
        trades = pd.DataFrame({"date": price.index, "signal": signal.values, "return": strat_ret.values})
        return trades.dropna().reset_index(drop=True), pd.Series(equity, index=price.index, name="equity")
