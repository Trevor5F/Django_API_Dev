import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ads.models import Ad, User, Category
from ads.permissions import AdUpdateDeletePermission
from ads.serializers.ad import AdSerializer, AdDestroySerializer, AdDetailSerializer


# Если вы хотите указать другой набор данных или применить какие-либо фильтры, вы можете явно указать `queryset`.
# Например, `queryset = Ad.objects.filter(is_published=True)` ограничит вывод только активных вакансий.

class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat", [])
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("name")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        price_to = request.GET.get("price_to")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=int(price_from))
        if price_to:
            self.queryset = self.queryset.filter(price__lte=int(price_to))

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ('name', 'author', 'price', 'description', 'is_published', 'category')

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        if ad_data['is_published'] is True:
            return JsonResponse({"error": "bad status"}, status=400)

        new_ad = Ad.objects.create(
            name=ad_data['name'],
            author=get_object_or_404(User, pk=ad_data["author_id"]),  # переопределяем поле на author_id
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            category=get_object_or_404(Category, pk=ad_data["category_id"]),
        )

        return JsonResponse({
            'id': new_ad.id,
            'name': new_ad.name,
            'author_id': new_ad.author_id,
            'author': new_ad.author.username,
            'price': new_ad.price,
            'description': new_ad.description,
            'is_published': new_ad.is_published,
            'category_id': new_ad.category_id,
            'image': new_ad.image.url if new_ad.image else None},
            safe=False)


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]
    serializer_class = AdSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]


class AdUploadImageView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def put(self, request, *args, **kwargs):
        ad = self.get_object()
        serializer = self.serializer_class(ad, data=request.data, partial=True)  # partial - частичное обновление

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
