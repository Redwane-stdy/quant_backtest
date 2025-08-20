from data.sample_data import load_ohlcv
from strategies.momentum_strategies import SimpleMomentum
from strategies.mean_reversion import ZScoreReversion

def test_momentum_runs():
    df = load_ohlcv()
    trades, equity = SimpleMomentum(lookback=10).run(df)
    assert len(trades) > 10
    assert equity.iloc[-1] > 0

def test_mean_reversion_runs():
    df = load_ohlcv()
    trades, equity = ZScoreReversion(lookback=10).run(df)
    assert len(trades) > 10
    assert equity.iloc[-1] > 0
