from django.db import models


class Agency(models.Model):
    code_commune = models.CharField(max_length=255, null=True)
    picture_url = models.CharField(max_length=255, null=True)
    agent = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["code_commune"]),
        ]

        verbose_name_plural = "Agencies"
