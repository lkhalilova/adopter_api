import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import AdopterSerializer
from .models import Adopter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsCustomAdminUser


class CustomPaginator(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10


class AdopterListView(ReadOnlyModelViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    permission_classes = (IsAuthenticated, IsCustomAdminUser)
    pagination_class = CustomPaginator
    search_fields = ["last_name", "city"]
    ordering_fields = ['city']
    filter_backends = [
        SearchFilter, OrderingFilter
    ]






