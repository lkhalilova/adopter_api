import django_filters
from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .models import Pet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import PetCreateSerializer, DogAgeReadSerializer, PetReadSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg, Max, Min
from django.views import View
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from typing import Any, List
from urllib.request import Request
from utils.permissions import IsCustomAdminUser
from utils.filters import IsOwnerFilterBackend


class CustomPaginator(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10


class PetFilter(django_filters.FilterSet):
    temporal_owner_id = django_filters.NumberFilter(field_name="owner__id")
    requested_pet__approved = django_filters.BooleanFilter(field_name="requested_pet__approved")

    class Meta:
        model = Pet
        fields = {
            'name': ['exact'],
            'species': ['exact'],
            'age': ['gte', 'lte', 'gt', 'lt', 'exact'],
            'city': ['exact'],
            'gender': ['exact'],
        }


class PetListView(ModelViewSet):
    queryset = Pet.objects.all()
    filterset_class = PetFilter
    pagination_class = CustomPaginator
    search_fields = ['name', 'species', 'age', 'gender', "city", '@description']
    ordering_fields = ['species', 'gender', 'city']
    filter_backends = [
        IsOwnerFilterBackend,
        django_filters.rest_framework.DjangoFilterBackend,
        SearchFilter, OrderingFilter
    ]

    def get_permissions(self) -> List[BasePermission]:
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsCustomAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PetReadSerializer
        return PetCreateSerializer

    @action(detail=False, methods=["GET"])
    def urgent_adoption_pets_list(self, request, *args, **kwargs):
        data = self.queryset.filter(needs_an_urgent_adoption=True)
        serializer = PetReadSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=["GET"])
    def get_real_dog_age(self, request, *args, **kwargs):
        data = self.queryset.filter(species='dog')
        serializer = DogAgeReadSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=["GET"])
    def get_age_statistics(self, request, *args, **kwargs):
        """
        Returns age statistics values
        based on all registered pets
        """
        statistics = Pet.objects.aggregate(
            avg_age=Avg('age'),
            max_age=Max('age'),
            min_age=Min('age')
        )
        return Response(statistics)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="temporal_owner_id",
                type=OpenApiTypes.INT,
                description="Filter pets by temporal owner id (ex. ?temporal_owner_id=2)",
            ),
            OpenApiParameter(
                name="requested_pet__approved",
                type=OpenApiTypes.BOOL,
                description="Filter adopted pets (ex. ?requested_pet__approved=True)",
            ),
        ],
        responses={200: PetReadSerializer(many=True)},
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        filter_params = request.query_params.dict()
        filterset = PetFilter(data=filter_params, queryset=queryset)

        if filterset.is_valid():
            queryset = filterset.qs

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class CitySelectView(View):
    """
    this view helps users to search for a pet depends on a city they choose
    """
    def get(self, request):
        cities = Pet.objects.values_list('city', flat=True).distinct()
        return render(request, 'pet/city_select.html', {'cities': cities})

    def post(self, request):
        selected_city = request.POST.get('city')  # get the selected city
        if selected_city:
            return redirect('city_pets', city=selected_city)
        return redirect('city_select')


class CityPetListView(View):
    """
    This view returns the html template with a list of pets depends on a city users
    have chosen previously
    """
    def get(self, request, city):
        pets = Pet.objects.filter(city=city)  # get a pet list for the city selected
        return render(request, 'pet/city_pets.html', {'city': city, 'pets': pets})




