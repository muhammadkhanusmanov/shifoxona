from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from apis.views import (BranchImg,DoctorImg,
   DoctorView,Resption,PatientsView
)


schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API Documentation for your project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourdomain.tld"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doctor/img/<str:id>', DoctorImg.as_view()),
    path('branch/img/<str:id>', BranchImg.as_view()),
    path('doctors/',DoctorView.as_view()),
    path('branch/dcs/',DoctorView.as_view()),
    path('dc/patients/',Resption.as_view()),
    path('add/patient/',Resption.as_view()),
    path('ph/patients/',PatientsView.as_view()),

]
