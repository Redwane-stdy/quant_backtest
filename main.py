import argparse
from pathlib import Path
from data.sample_data import load_ohlcv
from strategies.momentum_strategies import SimpleMomentum
from strategies.mean_reversion import ZScoreReversion
from strategies.arbitrage_strategies import PairStatArb
from utils.performance_analytics import compute_performance_report
from utils.plotting_utils import plot_equity_curve, plot_drawdowns, plot_monthly_heatmap

STRATEGY_MAP = {
    "momentum": SimpleMomentum,
    "mean_reversion": ZScoreReversion,
    "stat_arb": PairStatArb,
}

def parse_args():
    p = argparse.ArgumentParser(description="Academic Quant Backtester")
    p.add_argument("--symbols", nargs="+", default=["SAMPLE"], 
                    help="Un ou plusieurs tickers (ex: AAPL MSFT pour stat_arb)")
    p.add_argument("--strategy", type=str, choices=list(STRATEGY_MAP.keys()), default="momentum")
    p.add_argument("--start", type=str, default="2020-01-01")
    p.add_argument("--end", type=str, default="2022-12-31")
    p.add_argument("--capital", type=float, default=100_000.0)
    p.add_argument("--risk_per_trade", type=float, default=0.01)
    p.add_argument("--lookback", type=int, default=20)
    return p.parse_args()

def run():
    args = parse_args()

    if args.strategy == "stat_arb":
        if len(args.symbols) != 2:
            raise ValueError("La stratégie stat_arb nécessite exactement 2 symboles.")
        df1 = load_ohlcv(args.symbols[0], args.start, args.end, freq="D").dropna()
        df2 = load_ohlcv(args.symbols[1], args.start, args.end, freq="D").dropna()
    else:
        df1 = load_ohlcv(args.symbols[0], args.start, args.end, freq="D").dropna()
        df2 = None

    StrategyClass = STRATEGY_MAP[args.strategy]
    strat = StrategyClass(lookback=args.lookback, capital=args.capital, risk_fraction=args.risk_per_trade)

    if args.strategy == "stat_arb":
        trades, equity = strat.run_pair(df1, df2)
        out_prefix = f"{args.symbols[0]}_{args.symbols[1]}"
    else:
        trades, equity = strat.run(df1)
        out_prefix = args.symbols[0]

    report = compute_performance_report(equity, trades)

    outdir = Path("results")
    (outdir / "backtest_results").mkdir(parents=True, exist_ok=True)
    (outdir / "performance_reports").mkdir(parents=True, exist_ok=True)
    (outdir / "visualizations").mkdir(parents=True, exist_ok=True)

    equity.to_csv(outdir / "backtest_results" / f"equity_{out_prefix}_{args.strategy}.csv", index=True)
    trades.to_csv(outdir / "backtest_results" / f"trades_{out_prefix}_{args.strategy}.csv", index=False)
    report.to_csv(outdir / "performance_reports" / f"report_{out_prefix}_{args.strategy}.csv")

    plot_equity_curve(equity, title=f"Equity Curve - {out_prefix} - {args.strategy}",
                      savepath=outdir / "visualizations" / f"equity_{out_prefix}_{args.strategy}.png")
    plot_drawdowns(equity, title=f"Drawdowns - {out_prefix} - {args.strategy}",
                   savepath=outdir / "visualizations" / f"drawdowns_{out_prefix}_{args.strategy}.png")
    plot_monthly_heatmap(equity, title=f"Monthly Returns - {out_prefix} - {args.strategy}",
                         savepath=outdir / "visualizations" / f"monthly_{out_prefix}_{args.strategy}.png")

    print("Backtest terminé.")
    print(report)


if __name__ == "__main__":
    run()


def apply_trade_costs(price, direction, fees, slippage):
    """
    Applique frais et slippage sur le prix exécuté.
    direction: 1 = achat, -1 = vente
    """
    price_exec = price * (1 + direction * slippage)
    price_exec *= (1 + fees * direction)
    return price_exec
