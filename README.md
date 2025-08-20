# Quantitative Trading Backtester

Projet perso pour backtester des stratégies quantitatives sur OHLCV.
Inclut moteur de backtest, métriques de risque, graphiques, notebooks et tests.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

## Exécution rapide
```bash
python main.py --symbol SAMPLE --strategy momentum --start 2020-01-01 --end 2022-12-31
# Stratégies: momentum | mean_reversion | stat_arb
```

La strategie d'arbitrage n'est pas encore implementé et le chargement des données depuis Yahoo Finance


Les sorties sont sauvegardées sous `results/`.
