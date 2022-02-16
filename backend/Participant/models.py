from django.db import models

# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)

    def to_dict(self):
        return {"name": self.name, "wins": self.wins, "losses": self.losses}

    def __str__(self):
        return f"Participant: {self.name}"