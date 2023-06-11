from rest_framework.routers import SimpleRouter
from .views import AdopterListView
from django.urls import path
from .telegram import telegram_webhook

urlpatterns = [
    path('api/telegram/', telegram_webhook, name='telegram-api'),
]

router = SimpleRouter()
router.register("", AdopterListView)

urlpatterns += router.urls
