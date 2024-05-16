from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from .models import Doctor,Branch,Patients
from django.contrib.auth.models import User

class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class PatientsSerializer(ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'