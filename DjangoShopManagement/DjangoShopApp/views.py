from django.shortcuts import render
from rest_framework import viewsets, generics

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from DjangoShopApp.models import Company, CompanyBank, Product, ProductDetails
from DjangoShopApp.serializers import CompanySerliazer, CompanyBankSerializer, ProductSerliazer, \
    ProductDetailsSerializer, ProductDetailsSerializerSimple


class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerliazer(company,many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerliazer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error": False,"message": "Company Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Data"}
        return Response(dict_response)

    def update(self,request,pk=None):
        try:
            queryset=Company.objects.all()
            company=get_object_or_404(queryset,pk=pk)
            serializer=CompanySerliazer(company,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Successfully Updated Company Data"}
        except:
            dict_response = {"error": True, "message": "Error During Updating Company Data"}

        return Response(dict_response)


class CompanyBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error": False,"message": "Company Bank Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Bank Data"}
        return Response(dict_response)

    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company Bank List Data", "data": serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companybank,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companybank,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerliazer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Company.objects.filter(name=name)


class ProductViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request):
        try:
            serializer = ProductSerliazer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            product_id=serializer.data['id'];
            #Access the serializer Id which save database table
            #print(product_id)

            #Adding and saving Id into Product details serializer
            product_details_list=[]
            for product_details in request.data["product_details"]:
                print(product_details)

                #adding producr id which will work for product serializer
                product_details["product_id"]=product_id
                product_details_list.append(product_details)
                print(product_details)

            serializer2=ProductDetailsSerializer(data=product_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            dict_response={"error": False,"message": "Product Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Product Data"}
        return Response(dict_response)

    def list(self, request):
        product = Product.objects.all()
        serializer = ProductSerliazer(product, many=True, context={"request": request})

        product_data=serializer.data
        newproductlist=[]
        #Adding extra keys for product details in product
        for product in product_data:

            #Accessing all the product details of current product id
            product_details=ProductDetails.objects.filter(product_id=product["id"])
            product_details_serializers=ProductDetailsSerializerSimple(product_details,many=True)
            product["product_details"]=product_details_serializers.data
            newproductlist.append(product)


        response_dict = {"error": False, "message": "All Product List Data", "data": newproductlist}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=Product.objects.all()
        product=get_object_or_404(queryset,pk=pk)
        serializer=ProductSerliazer(product,context={"request":request})

        serializer_data=serializer.data
        # Accessing all the product details of current product id
        product_details = ProductDetails.objects.filter(product_id=serializer_data["id"])
        product_details_serializers = ProductDetailsSerializerSimple(product_details, many=True)
        serializer_data["product_details"] = product_details_serializers.data

        return Response({"error":False,"message":"Single Data Fetch","data":serializer_data})

    def update(self,request,pk=None):
        queryset=Product.objects.all()
        product=get_object_or_404(queryset,pk=pk)
        serializer=ProductSerliazer(product,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})


company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})

