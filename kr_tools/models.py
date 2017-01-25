from django.db import models

class Shop(models.Model):
    link = models.CharField()

class Card(models.Model):
    name = models.CharField()
