from django.contrib import admin
from .models import (Doctor,Branch)

admin.site.register([Doctor,Branch])
