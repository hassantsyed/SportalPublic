from django.db import models
from Account.models import Account

import uuid

# Create your models here.
class Crowd(models.Model):
    ooid = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    accounts = models.ManyToManyField(Account, blank=True)

    def to_dict(self):
        return {"ooid": self.ooid, "name": self.name}

    def __str__(self):
        return f"Crowd: {self.name}"