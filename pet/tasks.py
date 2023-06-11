import requests
from celery import shared_task
from .models import Pet
import random
from adoption_request.models import AdoptionRequest
from adopter.models import AnonymousUser
from adopter_bot.settings import TELEGRAM_BOT_TOKEN, TG_BASE_URL


@shared_task
def send_urgent_adoption_notification():
    """
    Sends every_day telegram notification with random Pet
    object that doesn't have related AdoptionRequest object.
    AnonymousUser object can create an adoption request on
    every Pet object by pressing "Create Adoption Request" button.
    """
    anonymous_users = AnonymousUser.objects.all()
    adoption_requests = AdoptionRequest.objects.all()
    requested_pets = [request.pet for request in adoption_requests]
    pets = Pet.objects.all()
    available_pets = [pet for pet in pets if pet not in requested_pets]

    if available_pets:
        pet = random.choice(pets)
        photo_path = pet.photo.path
        message = f"Name: {pet.name}\n" \
                  f"Species: {pet.species}\n" \
                  f"Age: {pet.age} {'місяців' if pet.age_in_months else 'років'}\n" \
                  f"Gender: {pet.gender}\n" \
                  f"City: {pet.city}\n" \
                  f"Description: {pet.description}"

        for anonymous_user in anonymous_users:
            chat_id = anonymous_user.chat_id
            photo_id_data = {
                "chat_id": chat_id,
                "photo_path": photo_path,
            }
            button = {
                "text": "Create Adoption Request",
                "callback_data": f"create_request_{pet.id}"
            }
            markup = {
                "inline:keyboard": [[button]]
            }
            text_id_data = {
                "chat_id": chat_id,
                "text": message,
                "reply_markup": markup
            }
            requests.post(f"{TG_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendPhoto", json=photo_id_data)
            requests.post(f"{TG_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", json=text_id_data)
            return "ok"




