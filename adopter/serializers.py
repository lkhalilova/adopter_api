from rest_framework import serializers
from .models import Adopter


class AdopterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adopter
        fields = "__all__"




