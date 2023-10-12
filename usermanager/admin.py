from django.contrib import admin
from .models import CustomUser, SuperAdmin

admin.site.register(CustomUser)
admin.site.register(SuperAdmin)
