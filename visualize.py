import json
import matplotlib.pyplot as plt
from collections import defaultdict


def plot_win_rates(stats_path="stats.json"):
    with open(stats_path, "r") as f:
        stats = json.load(f)

    personalities = []
    win_rates = []

    for name, data in stats.items():
        total = sum(data.values())
        if total == 0:
            continue
        win_rate = data["wins"] / total * 100
        personalities.append(name)
        win_rates.append(win_rate)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(personalities, win_rates, color="mediumslateblue")
    plt.title("♟️ Personality Win Rates")
    plt.ylabel("Win Rate (%)")
    plt.ylim(0, 100)

    for bar, rate in zip(bars, win_rates):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{rate:.1f}%", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def plot_weight_evolution(history_path="weight_history.json", personality="machine"):
    data = defaultdict(list)
    games = []

    try:
        with open(history_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry["personality"] != personality:
                    continue
                games.append(entry["game"])
                for trait, value in entry["weights"].items():
                    data[trait].append(value)
    except FileNotFoundError:
        print("No history file found. Play some games first to generate weight history.")
        return

    if not games:
        print(f"No history entries for personality: {personality}")
        return

    plt.figure(figsize=(10, 5))
    for trait, values in data.items():
        plt.plot(games, values, label=trait, linewidth=2)

    plt.title(f"🧬 Weight Evolution for '{personality}'")
    plt.xlabel("Games Played")
    plt.ylabel("Weight Value")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
