from django.db import models
from temporal_owner.models import TemporalOwner


class Pet(models.Model):
    GENDER = [
        ("F", "Female"),
        ("M", "Male"),
    ]
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    age = models.IntegerField()
    age_in_months = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    description = models.TextField()
    photo = models.ImageField(upload_to='staticfiles/')
    owner = models.ForeignKey(TemporalOwner, related_name="temporal_owner", on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    needs_an_urgent_adoption = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.species} - {self.name} , {self.gender}, {self.age}, {self.city}"

    class Meta:
        ordering = ["-needs_an_urgent_adoption"]

