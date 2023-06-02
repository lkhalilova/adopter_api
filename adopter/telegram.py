from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from adopter_bot.settings import TG_BASE_URL, TELEGRAM_BOT_TOKEN
from adoption_request.serializers import AdoptionRequestCreateSerializer
from pet.models import Pet
from .models import AnonymousUser


class TelegramWebhookMessageController:
    """
    This match case activates the celery task at pet/tasks.py
    """
    @staticmethod
    def handle_webhook(request):
        message = request.data.get('message', {})
        text = message.get('text', '')

        response_message = ""

        match text:
            case '/start':
                chat_id = message.get('chat', {}).get('id')

                try:
                    anonymous_user = AnonymousUser.objects.get(chat_id=chat_id)
                except AnonymousUser.DoesNotExist:
                    # Create a new AnonymousUser if it doesn't exist
                    anonymous_user = AnonymousUser.objects.create(chat_id=chat_id)

                response_message = "Вітаю! Тепер ви будете отримувати повідомлення та " \
                                   "пропозиції щодо тварин, які потребують прихистку!"

            case _:
                response_message = "Invalid command"
                return Response({"message": response_message})

        text_id_data = {
            "chat_id": chat_id,
            "text": response_message
        }
        requests.post(f"{TG_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", json=text_id_data)

        return Response({"message": response_message})


class TelegramWebhookCallbackController:
    """
    This match case processes the celery task at pet/tasks.py
    """
    @staticmethod
    def handle_webhook(request):
        callback_query = request.data.get('callback_query', {})
        callback_data = callback_query.get('data', '')

        response_message = ""

        match callback_data:
            case "create_request_{pet.id}":
                try:
                    pet_id = int(callback_data.split('_')[2])
                    pet = Pet.objects.get(id=pet_id)
                except (IndexError, ValueError, Pet.DoesNotExist):
                    return Response({"error": "Invalid callback data"}, status=status.HTTP_400_BAD_REQUEST)

                first_name = callback_query.get("from").get("first_name")
                last_name = callback_query.get("from").get("last_name")
                chat_id = callback_query.get("from").get("id")

                adopter_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "chat_id": chat_id
                }

                adoption_request_data = {
                    "pet": pet,
                    "adopter": adopter_data
                }

                serializer = AdoptionRequestCreateSerializer(data=adoption_request_data)

                if serializer.is_valid():
                    serializer.save()
                    response_message = "Adoption Request was created successfully!"
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            case _:
                response_message = "Invalid command"
                return Response({"message": response_message})

        text_id_data = {
            "chat_id": chat_id,
            "text": response_message
        }
        requests.post(f"{TG_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", json=text_id_data)

        return Response({"message": response_message})


@api_view(['POST'])
def telegram_webhook(request):
    if message := request.json.get("message"):
        handler = TelegramWebhookMessageController()
    elif callback := request.json.get("callback_query"):
        handler = TelegramWebhookCallbackController()
    else:
        return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    response = handler.handle_webhook(request)
    return Response({"message": response})