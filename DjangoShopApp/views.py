from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.

from rest_framework.response import Response
from DjangoShopApp.models import Company
from DjangoShopApp.serializers import CompanySerliazer


class CompanyViewSet(viewsets.ViewSet):

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerliazer(company,many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerliazer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            dict_response={"error": False,"message": "Company Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Data"}
        return Response(dict_response)


company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})

