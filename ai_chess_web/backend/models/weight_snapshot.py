from django.db import models

from ai_chess_web.backend.models.personality import Personality


class WeightSnapshot(models.Model):
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE)
    game_number = models.IntegerField()
    weights = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
