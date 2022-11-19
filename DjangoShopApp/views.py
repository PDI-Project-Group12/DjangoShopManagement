from django.shortcuts import render
from  rest_framework import viewsets

from DjangoShopApp.models import Company
from DjangoShopApp.serializers import CompanySerliazer


# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerliazer
