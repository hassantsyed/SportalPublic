from django.db import models
from League.models import League
from Participant.models import Participant
from django_prometheus.models import ExportModelOperationsMixin

# Create your models here.
class Match(ExportModelOperationsMixin('match'), models.Model):

    STATUS = [
        ("UPCOMING", "UPCOMING"), ("CANCELLED", "CANCELLED"), ("TEAM1", "TEAM1"), ("TEAM2", "TEAM2"), ("TIE", "TIE"), ("ONGOING", "ONGOING")
    ]

    LID = models.ForeignKey(League, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="team2")
    date = models.DateTimeField()
    order = models.IntegerField(default=0)
    status = models.TextField(choices=STATUS)
    apiID = models.IntegerField(default=0)
    result = models.CharField(blank=True, default="", null=True, max_length=255)

    class Meta:
        unique_together = ['team1', 'team2', 'date']
        ordering = ['-date', 'order']

    def to_dict(self):
        return {"MID": self.id, "team1": self.team1.to_dict(), "team2": self.team2.to_dict(), "date": self.date, "status": self.status, "LID": self.LID.pk, "result": self.result}

    def __str__(self):
        return f"Match: {self.team1.name} v. {self.team2.name}"
