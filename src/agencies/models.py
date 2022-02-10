from django.db import models


class Agency(models.Model):
    picture_url = models.CharField(max_length=255, null=True)
    agent = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True)

    class Meta:

        verbose_name_plural = "Agencies"


class Pricing(models.Model):
    name = models.CharField(max_length=255, null=False)
    min_population = models.PositiveIntegerField(null=False)
    max_population = models.PositiveIntegerField(null=False)
    pricing = models.FloatField(null=False)
