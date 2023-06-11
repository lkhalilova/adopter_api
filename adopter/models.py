from django.db import models


class AnonymousUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return str(self.chat_id)


class Adopter(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ["first_name", "last_name"]




