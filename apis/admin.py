from django.contrib import admin
from .models import (Doctor,Branch,Patients)

admin.site.register([Doctor,Branch,Patients])

