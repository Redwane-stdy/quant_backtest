from data.sample_data import load_ohlcv
from strategies.momentum_strategies import SimpleMomentum

def test_backtest_equity_monotonicity():
    df = load_ohlcv()
    trades, equity = SimpleMomentum(lookback=5).run(df)
    assert equity.isna().sum() == 0
    assert (equity > 0).all()
