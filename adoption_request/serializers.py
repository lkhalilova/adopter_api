from rest_framework import serializers
from .models import AdoptionRequest
from adopter.serializers import AdopterSerializer
from adopter.models import Adopter
from pet.serializers import PetReadSerializer


class AdoptionRequestReadSerializer(serializers.ModelSerializer):
    pet = PetReadSerializer()

    class Meta:
        model = AdoptionRequest
        fields = ['pet', 'adopter', 'approved', 'created_at']
        depth = 2


class AdoptionRequestCreateSerializer(serializers.ModelSerializer):
    adopter = AdopterSerializer()

    class Meta:
        model = AdoptionRequest
        fields = ['pet', 'adopter', 'created_at']

    def create(self, validated_data):
        """
        Adopter object is created every time AdoptionRequest object
        is created. No authentication required.
        """
        pet_data = validated_data.get('pet')
        approved = validated_data.get('approved', False)
        created_at = validated_data.get('created_at')

        adopter_data = validated_data.get('adopter')

        adopter = Adopter.objects.create(**adopter_data)

        adoption_request = AdoptionRequest.objects.create(
            pet=pet_data,
            adopter=adopter,
            approved=approved,
            created_at=created_at
        )

        return adoption_request


class ApproveAdoptionRequestSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = ('id', 'approved', 'created_at')





