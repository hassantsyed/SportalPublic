from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

# Create your models here.
class Account(ExportModelOperationsMixin('account'), models.Model):
    GID = models.CharField(max_length = 255, unique = True)
