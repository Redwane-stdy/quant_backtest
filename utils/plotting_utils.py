import matplotlib.pyplot as plt
import pandas as pd

def _save_or_show(savepath):
    if savepath:
        plt.savefig(savepath, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

def plot_equity_curve(equity: pd.Series, title: str = "Equity Curve", savepath=None):
    plt.figure(figsize=(10, 4))
    equity.plot()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Equity")
    _save_or_show(savepath)

def plot_drawdowns(equity: pd.Series, title: str = "Drawdowns", savepath=None):
    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0
    plt.figure(figsize=(10, 3.5))
    drawdown.plot()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    _save_or_show(savepath)

def plot_monthly_heatmap(equity: pd.Series, title: str = "Monthly Returns", savepath=None):
    ret = equity.pct_change().dropna()
    monthly = ret.resample("ME").apply(lambda x: (1 + x).prod() - 1)
    table = monthly.to_frame("ret")
    table["Year"] = table.index.year
    table["Month"] = table.index.month
    pivot = table.pivot(index="Year", columns="Month", values="ret").fillna(0.0)

    plt.figure(figsize=(10, 4))
    plt.imshow(pivot.values, aspect="auto", interpolation="nearest")
    plt.xticks(range(0, 12), ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.title(title)
    plt.colorbar(label="Return")
    _save_or_show(savepath)
