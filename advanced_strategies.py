from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class VolatilityTargeting:
    target_vol: float = 0.10
    lookback: int = 20
    min_leverage: float = 0.2
    max_leverage: float = 3.0

    def scale_positions(self, returns: pd.Series) -> pd.Series:
        vol = returns.rolling(self.lookback).std() * np.sqrt(252)
        lev = self.target_vol / vol
        lev = lev.clip(self.min_leverage, self.max_leverage)
        return lev.fillna(self.min_leverage)
