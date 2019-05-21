from django.db import models


class Suit(models.Model):
    url = models.CharField(max_length=1000)
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=150)
    fit = models.CharField(max_length=150)
    material = models.CharField(max_length=150)
    image = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Suit scraped from website"
