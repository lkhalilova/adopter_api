from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PetListView, CitySelectView, CityPetListView

router = SimpleRouter()
router.register("", PetListView)

urlpatterns = [
    path('city/', CitySelectView.as_view(), name='city_select'),
    path('city/<str:city>/', CityPetListView.as_view(), name='city_pets'),
    path('', include(router.urls)),
]


