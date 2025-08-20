# Documentation des stratégies

## Momentum
- Idée : s'exposer quand l'actif a performé positivement sur la fenêtre lookback.
- Signal : ret_{lookback} > 0 -> long; sinon cash.

## Mean Reversion (Z-Score)
- Idée : retour à la moyenne des rendements journaliers.
- Signal : z < -1 -> long; z > 1 -> short.

## Pairs Trading (Stat Arb)
- Idée : exploiter l'écart relatif entre deux séries corrélées.
- Signal : trader le z-score du spread cumulé.
