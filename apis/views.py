
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


from .serialazers import DoctorSerializer,BranchSerializer,PatientsSerializer
from .models import Doctor,Branch,Patients

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
    @swagger_auto_schema(
        
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    'doctors': openapi.Schema(type=openapi.TYPE_OBJECT, example={'name': '', 'branch':1,'desc':'','desc2':''}),
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                }
            ),
        },
        operation_description="The endpoint to get all doctors",
        )
    
    def get(self, request):
        try:
            doctors = Doctor.objects.all()
            doctors = DoctorSerializer(doctors, many=True).data
            rsp = []
            for doctor in doctors:
                doctor['img']=f'http://127.0.0.1:8000/doctor/{doctor["id"]}'
                rsp.append(doctor)
            return Response({'Status':True,'doctors':rsp},status=status.HTTP_200_OK)
        except:
            return Response({'Status':False},status=status.HTTP_400_BAD_REQUEST)
        
class BranchView(APIView):
    @swagger_auto_schema(
        request = {
            
        },
        
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    'branches': openapi.Schema(type=openapi.TYPE_OBJECT, example={'name': '', 'img':'url','desc':'','desc2':''}),
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                }
            ),
        },
        operation_description="The endpoint to get all branches",
        )
    
    def get(self,request):
        try:
            branches = Branch.objects.all()
            rsp = []
            branches = BranchSerializer(branches, many=True).data
            for branch in branches:
                branch['img']=f"http://127.0.0.1:8000/branch/{branch['id']}"
                rsp.append(branch)
            return Response({'Status':True,'branches':rsp},status=status.HTTP_200_OK)
        except:
            return Response({'Status':False},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        id = request.data.get('id', None)
        try:
            branch = Branch.objects.get(id=id)
            resp = {'branch':branch.name,'doctors':[]}
            dcs = Doctor.objects.filter(branch=branch)
            for dc in dcs:
                dc = DoctorSerializer(dc).data
                dc['img']=f'http://127.0.0.1:8000/doctor/{dc["id"]}'
                resp['doctors'].append(dc)
            return Response(resp, status=status.HTTP_200_OK)
        except:
            return Response({'Status':False},status=status.HTTP_400_BAD_REQUEST)


from datetime import datetime,timedelta

class Resption(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Doctor ID'),
        },
        required=['id']
    ), 
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=[
                    openapi.Schema(type=openapi.TYPE_OBJECT, example={
        "name":"",
        "adress":"",
        "doctor":"id",
        "phone":"",
        "book":"%Y-%m-%d %H:%M",
        "desc":"",
    }),
                ]
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                }
            ),
        },
        operation_description="The endpoint to get all branches",
        )
    def post(self,request):
        id = request.data.get('id', None)
        try:
            dc = Doctor.objects.get(id=id)
            pts = Patients.objects.filter(doctor=dc)
            rsp = []
            for pt in pts:
                sr_pt = PatientsSerializer(pt).data
                book_dt = datetime.strptime(sr_pt['book'],'%Y-%m-%d %H:%M') + timedelta(minutes=20)
                current_dt = datetime.now()
                print(1)
                if current_dt < book_dt:
                    rsp.append(sr_pt)
                else:
                    pt.delete()
            return Response(rsp, status=status.HTTP_200_OK)
        except:
            return Response({'Status':False},status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Patient name'),
            'adress': openapi.Schema(type=openapi.TYPE_STRING, description='Patient address'),
            'doctor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Doctor ID'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Patient phone number'),
            'book': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Appointment booking time'),
            'desc': openapi.Schema(type=openapi.TYPE_STRING, description='Appointment description'),
        },
        required=['name', 'adress', 'doctor', 'phone', 'book', 'desc']
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Patient appointment created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                }
            )
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Invalid data for patient appointment',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                }
            )
        )
    },
    operation_description='Create a new patient appointment',
)
    def put(self,request):
        data = request.data
        pt = PatientsSerializer(data=data)
        if pt.is_valid():
            pt.save()
            return Response({'Status':True},status=status.HTTP_201_CREATED)
        return Response({'Status':False},status=status.HTTP_400_BAD_REQUEST)

class PatientsView(APIView):
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Patient phone number'),
        },
        required=['phone']
    ),
    responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Patient name'),
                    'adress': openapi.Schema(type=openapi.TYPE_STRING, description='Patient address'),
                    'doctor': openapi.Schema(type=openapi.TYPE_OBJECT, description='Doctor'),
                    'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Patient phone number'),
                    'book': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Appointment booking time'),
                    'desc': openapi.Schema(type=openapi.TYPE_STRING, description='Appointment description'),
                },
            ),
        ),
    },
    operation_description='Retrieve patient appointments by phone number',
)
    
    def post(self, request):
        phone = request.data.get('phone',None)
        pts = Patients.objects.filter(phone=phone)
        rsp = []
        for pt in pts:
            sr_pt = PatientsSerializer(pt).data
            book_dt = datetime.strptime(sr_pt['book'],'%Y-%m-%d %H:%M') + timedelta(minutes=20)
            current_dt = datetime.now()
            if current_dt < book_dt:
                rsp.append(sr_pt)
            else:
                pt.delete()
        return Response(rsp, status=status.HTTP_200_OK)