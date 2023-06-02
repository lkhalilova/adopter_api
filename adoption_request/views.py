from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .serializers import AdoptionRequestCreateSerializer, AdoptionRequestReadSerializer, \
    ApproveAdoptionRequestSerializer
from .models import AdoptionRequest
from rest_framework.response import Response
from .tasks import send_adoption_update_notification
from rest_framework.decorators import action
from django.db.models import Count, Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from adopter.models import Adopter
from pet.models import Pet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from utils.permissions import IsCustomAdminUser
from typing import List
from rest_framework.filters import SearchFilter, OrderingFilter


class CustomPaginator(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10


class AdoptionRequestListView(ModelViewSet):
    queryset = AdoptionRequest.objects.all()
    pagination_class = CustomPaginator
    search_fields = ["requested_pet.id", "=adopter.chat_id", "=adopter.last_name"]
    ordering_fields = ['approved']
    filter_backends = [
        SearchFilter, OrderingFilter
    ]

    def get_permissions(self) -> List[BasePermission]:
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsCustomAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = AdoptionRequest.objects.all()

        approved = self.request.query_params.get('approved', None)
        if approved is not None:
            queryset = queryset.filter(approved=approved)

        species = self.request.query_params.get('species', None)
        if species is not None:
            queryset = queryset.filter(pet__species__icontains=species)

        min_age = self.request.query_params.get('min_age', None)
        max_age = self.request.query_params.get('max_age', None)

        if min_age is not None and max_age is not None:
            queryset = queryset.filter(pet__age__gte=min_age, pet__age__lte=max_age)

        date = self.request.query_params.get('year', None)
        if date is not None:
            queryset = queryset.filter(date__year=date)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AdoptionRequestReadSerializer
        return AdoptionRequestCreateSerializer

    @action(detail=False, methods=["GET"])
    def get_statistics(self, request, *args, **kwargs):
        """
        Provides the following statistics:
        - how many requests were approved per last month;
        - what pets species people are inclined to adopt the most;
        - in what age most pets are being adopted;
        - how many pets does need an urgent adoption;
        - which 3 cities have the biggest adoption demand
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        approved_count = AdoptionRequest.objects.filter(
            approved=True,
            created_at__range=(
                start_date, end_date)).count()
        species_counts = Pet.objects.values('species').annotate(
            count=Count('requested_pet', filter=Q(
                requested_pet__approved=True))).order_by('-count')[:1]
        most_adopted_species = species_counts[0]['species'] if species_counts else None

        age_counts = Pet.objects.filter(
            requested_pet__approved=True
        ).values('age').annotate(count=Count('requested_pet')).order_by('-count')[:1]
        most_adopted_age = age_counts[0]['age'] if age_counts else None

        urgent_adoption_count = Pet.objects.filter(
            needs_an_urgent_adoption=True,
            requested_pet__approved=False).count()

        city_counts = Adopter.objects.filter(
            adopter__approved=True
        ).values('city').annotate(count=Count('adopter')).order_by('-count')[:3]
        most_adopter_cities = [city['city'] for city in city_counts] if city_counts else None

        data = {
            'approved_count': approved_count,
            'most_adopted_species': most_adopted_species,
            'most_adopted_age': most_adopted_age,
            'urgent_adoption_count': urgent_adoption_count,
            'adoption_champion_cities': most_adopter_cities,
        }

        return JsonResponse(data)


class AdoptionRequestApproveView(ModelViewSet):
    """
    This view gives TemporalOwner(is_admin=True)
    objects access to approve or reject an adoption request
    which is accessible via id. Authentication is required.
    Whenever adoption request is updated, related
    Adopter object gets corresponding notification.
    """
    serializer_class = ApproveAdoptionRequestSerializer
    queryset = AdoptionRequest.objects.all()
    permission_classes = [IsAuthenticated, IsCustomAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        # celery task is being called here
        send_adoption_update_notification.delay(serializer.instance.id)

        return Response(serializer.data)




