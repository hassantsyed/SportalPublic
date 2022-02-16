from django.db import models

#make an enum for sports
# Create your models here.
class League(models.Model):

    SPORTS = [
        ("SOCCER", "SOCCER"), ("MMA", "MMA"), ("FOOTBALL", "FOOTBALL"), ("BASEBALL", "BASEBALL")
    ]

    sportName = models.TextField(choices=SPORTS)
    leagueName = models.CharField(max_length = 255)

    def to_dict(self):
        return {"sport": self.sportName, "league": self.leagueName}

    def __str__(self):
        return f"League: {self.leagueName}"