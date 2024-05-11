
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import HttpRequest,JsonResponse,FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serialazers import DoctorSerializer,BranchSerializer
from .models import Doctor,Branch

class BranchImg(APIView):
    def get(self,request,id:str):
        branch = Branch.objects.get(id=id)
        img = branch.img
        img = open(img.path, 'rb')
        return FileResponse(img)

class DoctorImg(APIView):
    def get(self,request,id:str):
        doctor = Doctor.objects.get(id=id)
        img = doctor.img
        img = open(img.path, 'rb')
        return FileResponse(img)
    
class DoctorView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT
    ),
    responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    'doctors': openapi.Schema(type=openapi.TYPE_OBJECT, example={'name': '', 'branch':1,'desc':'','desc2':''}),
                })
            },
    operation_description="The enpoint to get all doctors",
    )
    
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)