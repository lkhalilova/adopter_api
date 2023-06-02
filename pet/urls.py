from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PetListView, CitySelectView, CityPetListView
from django.conf.urls.static import static
from adopter_bot import settings


router = SimpleRouter()
router.register("", PetListView)

urlpatterns = [
    path('city/', CitySelectView.as_view(), name='city_select'),
    path('city/<str:city>/', CityPetListView.as_view(), name='city_pets'),
    path('', include(router.urls)),
]

# if settings.DEBUG:
#        urlpatterns += staticfiles(settings.MEDIA_URL,
#                              document_root=settings.MEDIA_ROOT)
