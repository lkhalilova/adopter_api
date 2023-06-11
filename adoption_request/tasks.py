from celery import shared_task
from adopter_bot.settings import TELEGRAM_BOT_TOKEN, TG_BASE_URL
from .models import AdoptionRequest
import requests


@shared_task
def send_adoption_update_notification(adoption_request_id):
    """
    Sends telegram notification on every adoption request approve or
    reject update
    """
    try:
        adoption_request = AdoptionRequest.objects.get(id=adoption_request_id)
        adopter = adoption_request.adopter
        message = f"Hello,{adopter.first_name},We would like to inform you that your adoption request " \
                  f"for the pet named {adoption_request.pet.name} has been " \
                  f"{'approved' if adoption_request.approved else 'rejected'}." \
                  f"Thank you for your interest in adopting a pet!Best regards,The Pet Shelter Team"
        text_id_data = {
            "chat_id": adoption_request.adopter.chat_id,
            "text": message
        }
        requests.post(f"{TG_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", json=text_id_data)
        return "ok"
    except AdoptionRequest.DoesNotExist:
        pass
