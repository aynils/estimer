from django.contrib import admin

from .models import Agency


class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    list_filter = ("name", "email")


admin.site.register(Agency, AgencyAdmin)
