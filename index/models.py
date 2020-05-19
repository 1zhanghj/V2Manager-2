from django.db import models

# Create your models here.

class V2rayConfig(models.Model):
    UUID = models.CharField(max_length=255, primary_key=True)
    Path = models.CharField(max_length=255)
    Log = models.CharField(max_length=255)
    Level = models.CharField(max_length=10)
    Port = models.CharField(max_length=15)
    Portocol = models.CharField(max_length=15)
    DataPortocol = models.CharField(max_length=15)