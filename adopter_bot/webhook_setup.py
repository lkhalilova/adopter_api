import requests
from pyngrok import ngrok


def setup_telegram_webhook(telegram_bot_token):
    ngrok_url = ngrok.connect(8000).public_url
    telegram_webhook_url = f"{ngrok_url}/adopter/api/telegram/"
    webhook_url = f"https://api.telegram.org/bot{telegram_bot_token}/setWebhook?url={telegram_webhook_url}"
    response = requests.get(webhook_url)
    print(response.json())