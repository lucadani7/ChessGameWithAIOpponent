import random
from ai_chess_web.backend.engine.personality_manager import PersonalityManager
from visualize import show_dashboard


PERSONALITIES = ["positionalist", "gambiteer", "grinder", "romantic", "machine"]


# Mock game simulation – replace with your actual game logic
def simulate_game(personality_name):
    result = random.choices(["win", "loss", "draw"], weights=[0.45, 0.4, 0.15])[0]
    print(f"🎮 Simulated {personality_name} → {result}")
    return result


def run_tournament(personality, rounds=20, manager=None):
    print(f"\n🏁 Running {rounds} games as {personality}")
    if manager is None:
        manager = PersonalityManager()

    for i in range(rounds):
        result = simulate_game(personality)
        manager.update_stats(personality, result)

    manager.log_personality_update(personality)

    show_dashboard(personality=personality)


def run_all_tournaments(rounds_per_style=20):
    pm = PersonalityManager()
    for personality in PERSONALITIES:
        run_tournament(personality, rounds=rounds_per_style, manager=pm)
