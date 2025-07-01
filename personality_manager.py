import json
import os
import random

from personality_utils import DEFAULT_STATS, DEFAULT_WEIGHTS


class PersonalityManager:
    def __init__(self, stats_path="stats.json", weights_path="weights.json", mutation_rate=0.02):
        self.stats_path = stats_path
        self.weights_path = weights_path
        self.mutation_rate = mutation_rate

        self.stats = self._load_or_create_file(self.stats_path, DEFAULT_STATS)
        self.weights = self._load_or_create_file(self.weights_path, DEFAULT_WEIGHTS)

    def _load_or_create_file(self, path, default_data):
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default_data, f, indent=2)
            return default_data.copy()
        with open(path, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.stats_path, "w") as f:
            json.dump(self.stats, f, indent=2)
        with open(self.weights_path, "w") as f:
            json.dump(self.weights, f, indent=2)

    def update_stats(self, personality, result):
        if result not in ["win", "loss", "draw"]:
            return
        self.stats[personality][result + "s"] += 1
        self.tune_weights(personality)
        self.save()

    def tune_weights(self, personality):
        stats = self.stats[personality]
        total_games = sum(stats.values())
        if total_games < 10:
            return  # Not enough data to adjust

        win_rate = stats["wins"] / total_games
        w = self.weights[personality]

        for key in w:
            if key == "risk_penalty":
                continue
            if win_rate < 0.3:
                w[key] += self.mutation_rate
            elif win_rate > 0.7:
                w[key] -= self.mutation_rate * 0.5
            # Clamp to [0.0, 1.0]
            w[key] = max(0.0, min(1.0, w[key]))

    def get_weights(self, personality):
        return self.weights.get(personality, DEFAULT_WEIGHTS["machine"])

    def choose_personality(self):
        return random.choice(list(self.weights.keys()))

    def reset_all(self):
        self.stats = DEFAULT_STATS.copy()
        self.weights = DEFAULT_WEIGHTS.copy()
        self.save()
        print("All stats and weights have been reset to defaults.")

    def get_win_rate(self, personality):
        s = self.stats[personality]
        total = sum(s.values())
        return round(s["wins"] / total * 100, 2) if total else 0

    def log_personality_update(self, personality):
        winrate = self.get_win_rate(personality)
        print(f"[🧠 {personality}] Win rate: {winrate}% | Weights: {self.weights[personality]}")

    def personality_summary(self):
        for p in self.weights:
            print(f"{p:<12} → Win Rate: {self.get_win_rate(p):>5}% | Weights: {self.weights[p]}")
