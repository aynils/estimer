from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "last_login")


admin.site.register(CustomUser, CustomUserAdmin)
