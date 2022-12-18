from rest_framework import generics , status


from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

from .utilities.globalSchema import GlobalSchema
from .utilities.localSchema import LocalSchema

from .models import localSchemaModel , globalSchemaModel
from .serializers import localSchemaSerializer , globalSchemaSerializer
from .utilities.APIutil import APIutil

from rest_framework.decorators import api_view

# Create your views here.

class localSchemaAPI(generics.GenericAPIView):
    def get_serializer_class(self):
        return localSchemaSerializer

    def get_queryset(self):
        return localSchemaModel.objects.all()
    
    def get(self,request):
        serislizer_class = self.get_serializer_class()
        serializer = serislizer_class(self.get_queryset() , many = True )
        return Response(serializer.data)

    def post(self,request):
        serislizer_class = self.get_serializer_class()
        # print(request.data)
        serializer = serislizer_class(data= request.data)
        # print(serializer.data)
        if(serializer.is_valid()):
          serializer.save()
          return Response(serializer.data)  
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            ls = localSchemaModel.objects.get(id = request.data["id"])
            ls.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self,request):
        try:
            ls = localSchemaModel.objects.get(id = request.data["id"])
        except:
            return Response(status= status.HTTP_404_NOT_FOUND)
        serislizer_class = self.get_serializer_class()
        serializer = serislizer_class(ls, data= request.data)
        # print("this the data recieved on request", request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)  
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)








class globalSchemaAPI(generics.GenericAPIView):
    def get_serializer_class(self):
        return globalSchemaSerializer

    def get_queryset(self):
        return globalSchemaModel.objects.all()
    
    def get(self,request):
        serislizer_class = self.get_serializer_class()
        serializer = serislizer_class(self.get_queryset() , many = True )
        return Response(serializer.data)

    def post(self, request):
        print(" this is the data recieved on post", request.data)
        serislizer_class = self.get_serializer_class()
        serializer = serislizer_class(data= request.data)

        if(serializer.is_valid()):
            serializer.save()
            print("this is the validated data ", serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            gs = globalSchemaModel.objects.get(id = request.data["id"])
            gs.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request):
        try:
            gs = globalSchemaModel.objects.get(id = request.data["id"])
        except:
            return Response(status= status.HTTP_404_NOT_FOUND)
        serislizer_class = self.get_serializer_class()
        serializer = serislizer_class(gs, data= request.data)
        # print("this the data recieved on request", request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)  
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def makeConnection(request):
    if request.method == 'POST':
        try:
            gsmi = globalSchemaModel.objects.get(id = request.data["id"])
            gs = GlobalSchema()
            gs.updateSchema(gsmi.schema)
            fkname = request.data["connection"]["fkname"]
            t1 = request.data["connection"]["t1"]
            t2 = request.data["connection"]["t2"]
            c1 = request.data["connection"]["c1"]
            c2 = request.data["connection"]["c2"]
            gs.make_connection(fkname,t1,t2,c1,c2)
            gsmi.schema = gs.getSchema()
            gsmi.save()
            return Response(request.data , status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("only post method is applicable", status=status.HTTP_403_FORBIDDEN)










