from django.db import models

from League.models import League
from Account.models import Account
from Match.models import Match
from django_prometheus.models import ExportModelOperationsMixin

# Create your models here.
class Pick(ExportModelOperationsMixin('pick'), models.Model):

    STATUS = [
        ("TEAM1", "TEAM1"), ("TEAM2", "TEAM2"), ("TIE", "TIE")
    ]

    LID = models.ForeignKey(League, on_delete=models.CASCADE)
    UID = models.ForeignKey(Account, on_delete=models.CASCADE)
    MID = models.ForeignKey(Match, on_delete=models.CASCADE)
    pick = models.TextField(choices=STATUS)


    def to_dict(self):
        res = {
            "uid": self.UID.pk,
            "leagueDetails": self.LID.to_dict(), 
            "matchDetails": self.MID.to_dict(), 
            "pick": self.pick
        }
        return res

    class Meta:
        unique_together = ['UID', 'MID']
        ordering = ["-MID__date", 'MID__order']
