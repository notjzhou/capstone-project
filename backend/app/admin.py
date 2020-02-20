from django.contrib import admin

# Register your models here.
from .models import Beat, Rap

admin.site.register(Beat)
admin.site.register(Rap)
