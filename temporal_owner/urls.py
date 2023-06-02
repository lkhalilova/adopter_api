from .views import CreateTemporalOwnerView, ManageTemporalOwnerView
from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("reqister/", CreateTemporalOwnerView.as_view(), name="register"),
    path("login/", views.obtain_auth_token, name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("manage/", ManageTemporalOwnerView.as_view(), name="manage"),
]

app_name = "temporal_owner"