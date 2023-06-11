import os
import io
from PIL import Image
from rest_framework import serializers
from .models import Pet
import base64
from django.core.files.base import ContentFile
from adopter_bot import settings
from adoption_request.models import AdoptionRequest
import uuid


class PetReadSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Adds clarification to Pet object description
        field depends on whether it has a related AdoptionRequest object that
        is not yet approved, is already approved or it doesn't have one,
        hence it can be created.
        """
        data = super().to_representation(instance)

        adoption_request = AdoptionRequest.objects.filter(pet=instance).first()

        if adoption_request:
            if not adoption_request.approved:
                data['description'] += " There is an ongoing adoption request for this pet that is not yet approved." \
                                      " Please, check on this pet later."
            else:
                data['description'] += " This pet has already been adopted. But there are other pets, who also " \
                                       "need a loving home. Please, continue searching."
        else:
            data['description'] += " This pet needs a loving home."

        return data

    class Meta:
        model = Pet
        fields = ("id", "name", "species", "age", "age_in_months", "gender", "city", "description",
                  "photo")


class PetCreateSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Pet
        fields = (
            "id", "name", "species", "age", "age_in_months", "gender", "city", "description",
            "photo", "needs_an_urgent_adoption", "owner"
        )

    def save_photo(self, photo_data):
        # Decoding photo to Base64 string
        imgstr = base64.b64encode(photo_data.read()).decode('utf-8')
        # Generating a unique filename for the photo
        ext = photo_data.name.split('.')[-1]
        photo_name = f"pet/{uuid.uuid4()}.{ext}"
        photo = ContentFile(base64.b64decode(imgstr), name=photo_name)

        # Changing photo size
        resized_photo = self.resize_image(photo, (800, 600))

        # Saving the photo
        photo_path = os.path.join(settings.STATIC_URL, photo_name)
        resized_photo.save(photo_path)

        # Returning the photo URL
        photo_url = os.path.join(settings.STATIC_URL, photo_name)
        return photo_url

    def resize_image(self, image, size):
        img = Image.open(io.BytesIO(image.read()))
        img.thumbnail(size, Image.ANTIALIAS)
        return img

    def create(self, validated_data):
        photo_data = validated_data.pop("photo")
        photo = self.save_photo(photo_data)

        validated_data["photo"] = photo
        pet = Pet.objects.create(**validated_data)

        return pet


class DogAgeReadSerializer(serializers.ModelSerializer):
    """
    Returns the dog age that is equivalent to a human's age,
    where 1 human year equals 7 dog years.
    """
    age = serializers.SerializerMethodField(method_name="get_dog_age", read_only=True)

    def get_dog_age(self, obj):
        if obj.age_in_months:
            if obj.age * 7 > 12:
                return f"{obj.age * 7 // 12} dog years"
            else:
                return f"{obj.age * 7} dog months"
        return f"{obj.age * 7} dog years"

    class Meta:
        model = Pet
        fields = ("name", "species", "age", "gender", "description", "photo", "city")





