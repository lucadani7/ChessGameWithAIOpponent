from django.db import models

from ai_chess_web.backend.models.personality import Personality


class GameResult(models.Model):
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=[("win", "Win"), ("loss", "Loss"), ("draw", "Draw")])
    timestamp = models.DateTimeField(auto_now_add=True)
