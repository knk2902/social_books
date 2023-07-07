from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFiles

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'password', 'fullname', 'dob', 'visibility', 'age']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedFiles)
