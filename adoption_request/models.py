from django.db import models
from pet.models import Pet
from adopter.models import Adopter


class AdoptionRequest(models.Model):
    pet = models.OneToOneField(Pet, related_name="requested_pet", on_delete=models.CASCADE)
    adopter = models.ForeignKey(Adopter, related_name="adopter", on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.adopter.first_name} {self.adopter.last_name} - " \
               f"{self.pet.name} {self.pet.species} {self.pet.city} "

    class Meta:
        ordering = ["approved"]
        unique_together = ["pet", "adopter"]
