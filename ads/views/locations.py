from rest_framework.viewsets import ModelViewSet

from ads.models import Location
from ads.serializers.location import LocationSerializer


class LocationViewSet(ModelViewSet):  # ModelViewSet - уже есть все методы CRUD
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
