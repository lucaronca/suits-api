from django.db import models


class Suit(models.Model):
    url = models.CharField(max_length=1000, primary_key=True)
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=150)
    fit = models.CharField(max_length=150)
    material = models.CharField(max_length=150)
    image = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Suit scraped from website"
        ordering = ['name']


class Price(models.Model):
    suit = models.ForeignKey(Suit, models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3, default='GBP')

    def __unicode__(self):
        return '{}{}'.format(self.currency, self.amount)
