import json
import os
import platform
import subprocess
from datetime import datetime

import matplotlib.pyplot as plt
from collections import defaultdict


def get_timestamped_path(filename_base, folder="reports", extension="png"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_base}_{timestamp}.{extension}"
    return os.path.join(folder, filename)


def open_file(filepath):
    match platform.system():
        case "Darwin":  # MacOS
            subprocess.run(["open", filepath])
        case "Windows":
            os.startfile(filepath)
        case "Linux":
            subprocess.run(["xdg-open", filepath])


def export_snapshot_json(personality, stats_path, weights_path, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    with open(stats_path, "r") as f:
        stats = json.load(f)
    with open(weights_path, "r") as f:
        weights = json.load(f)

    export = {
        "timestamp": timestamp,
        "personality": personality,
        "stats": stats.get(personality, {}),
        "weights": weights.get(personality, {})
    }

    filename = os.path.join(out_folder, f"profile_{personality}_{timestamp}.json")
    with open(filename, "w") as f:
        json.dump(export, f, indent=2)
    print(f"📝 Stats + weights snapshot saved to {filename}")


def show_dashboard(personality="machine", stats_path="stats.json", weights_path="weights.json"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_folder = os.path.join("reports", personality, f"session_{timestamp}")
    os.makedirs(out_folder, exist_ok=True)

    print(f"\n📊 Dashboard for personality: {personality}")
    plot_win_rates(stats_path=stats_path, export=True, out_folder=out_folder)
    plot_weight_evolution(personality=personality, export=True, out_folder=out_folder)
    export_snapshot_json(personality, stats_path, weights_path, out_folder)


def plot_win_rates(stats_path="stats.json", export=True, out_folder="reports"):
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
    if export:
        filepath = get_timestamped_path("win_rates", folder=out_folder)
        plt.savefig(filepath)
        open_file(filepath)
        print(f"📦 Win rate chart saved to {filepath}")
    plt.show()


def plot_weight_evolution(history_path="weight_history.json", personality="machine", export=True, out_folder="reports"):
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
        print("⚠️ No weight history file found.")
        return

    if not games:
        print(f"⚠️ No history entries for personality: {personality}")
        return

    plt.figure(figsize=(10, 5))
    for trait, values in data.items():
        plt.plot(games, values, label=trait, linewidth=2)

    plt.title(f"🧬 Weight Evolution: '{personality}'")
    plt.xlabel("Games Played")
    plt.ylabel("Weight Value")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if export:
        filepath = get_timestamped_path(f"weight_evolution_{personality}", folder=out_folder)
        plt.savefig(filepath)
        open_file(filepath)
        print(f"📦 Weight evolution chart saved to {filepath}")
    plt.show()
