from .models import TemporalOwner
from .serializers import TemporalOwnerSerializer, AuthTokenSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateTemporalOwnerView(generics.CreateAPIView):
    serializer_class = TemporalOwnerSerializer


class ManageTemporalOwnerView(generics.RetrieveUpdateAPIView):
    serializer_class = TemporalOwnerSerializer
    queryset = TemporalOwner.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user






















