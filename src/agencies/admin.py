from django.contrib import admin

from .models import Agency, Pricing


class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    list_filter = ("name", "email")


class PricingAdmin(admin.ModelAdmin):
    list_display = ("name", "min_population", "max_population", "pricing")
    list_filter = ("name", "min_population", "max_population", "pricing")


admin.site.register(Agency, AgencyAdmin)
admin.site.register(Pricing, PricingAdmin)
