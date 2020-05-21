from django.db import models

# Create your models here.

class V2rayConfig(models.Model):
    UUID = models.CharField(max_length = 255, primary_key = True)
    Path = models.CharField(max_length = 255)
    Log = models.CharField(max_length = 255)
    Level = models.CharField(max_length = 10)
    Port = models.CharField(max_length = 15)
    Protocol = models.CharField(max_length = 15)
    DataProtocol = models.CharField(max_length = 15)

class V2rayShadowsocks(models.Model):
    ID = models.CharField(max_length = 255, primary_key = True)
    Password = models.CharField(max_length = 18)