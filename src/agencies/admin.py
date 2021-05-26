from django.contrib import admin

from .models import Agency

class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name","email", "code_commune")
    list_filter = ("name","email", "code_commune")


admin.site.register(Agency, AgencyAdmin)
