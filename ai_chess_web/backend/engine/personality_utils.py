import json
import os

DEFAULT_STATS = {
    "positionalist": {"wins": 0, "losses": 0, "draws": 0},
    "gambiteer": {"wins": 0, "losses": 0, "draws": 0},
    "grinder": {"wins": 0, "losses": 0, "draws": 0},
    "romantic": {"wins": 0, "losses": 0, "draws": 0},
    "machine": {"wins": 0, "losses": 0, "draws": 0}
}

DEFAULT_WEIGHTS = {
    "positionalist": {"structure": 0.6, "mobility": 0.3, "center": 0.4},
    "gambiteer": {"structure": 0.2, "mobility": 0.7, "center": 0.1, "risk_penalty": -0.1},
    "grinder": {"structure": 0.7, "mobility": 0.4, "center": 0.3},
    "romantic": {"structure": 0.1, "mobility": 0.8, "center": 0.2},
    "machine": {"structure": 0.4, "mobility": 0.5, "center": 0.25}
}


def ensure_weights_file(path="weights.json", reset=False):
    if not reset and os.path.exists(path):
        print("weights.json already exists and will remain untouched.")
    else:
        with open(path, "w") as f:
            json.dump(DEFAULT_WEIGHTS, f, indent=2)
        print("weights.json has been created/reset.")


def ensure_stats_file(path="stats.json", reset=False):
    if not reset and os.path.exists(path):
        print("stats.json already exists and will remain untouched.")
    else:
        with open(path, "w") as f:
            json.dump(DEFAULT_STATS, f, indent=2)
        print("stats.json has been created/reset.")
