import numpy as np
import pandas as pd

def _make_ohlcv(n: int, start_price: float = 100.0, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rets = rng.normal(0.0005, 0.01, size=n)
    prices = start_price * (1 + rets).cumprod()
    highs = prices * (1 + rng.normal(0.002, 0.004, size=n).clip(0, 0.05))
    lows  = prices * (1 - rng.normal(0.002, 0.004, size=n).clip(0, 0.05))
    opens = prices * (1 + rng.normal(0, 0.002, size=n))
    vols  = rng.integers(1e5, 1e6, size=n)
    df = pd.DataFrame({"Open": opens, "High": highs, "Low": lows, "Close": prices, "Volume": vols})
    return df

def load_ohlcv(symbol: str = "SAMPLE", start: str = "2020-01-01", end: str = "2022-12-31", freq: str = "D") -> pd.DataFrame:
    idx = pd.date_range(start=start, end=end, freq=freq)
    df = _make_ohlcv(len(idx))
    df.index = idx
    df["Symbol"] = symbol
    return df
