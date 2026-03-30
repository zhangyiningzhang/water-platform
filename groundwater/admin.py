# groundwater/admin.py
from django.contrib import admin
from .models import WellData

admin.site.register(WellData)