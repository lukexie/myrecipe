""" APIのビューセット """
from rest_framework import viewsets
from recipe.core.models import Cuisine, Foodstuff
from .serializer import CuisineSerializer, CuisineListSerializer, FoodstuffListSerializer

class CuisineViewSet(viewsets.ModelViewSet):
    """ メニュー REST API """
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = CuisineListSerializer
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)

        classification = self.request.query_params.get('classification')
        if classification:
            queryset = queryset.filter(classification=classification)

        kcal = self.request.query_params.get('kcal')
        if kcal:
            queryset = queryset.filter(ingestion_kcal__lte=kcal)

        return queryset

class FoodstuffViewSet(viewsets.ModelViewSet):
    """ 食材 REST API """
    queryset = Foodstuff.objects.distinct().order_by('name').values('name')
    serializer_class = FoodstuffListSerializer
