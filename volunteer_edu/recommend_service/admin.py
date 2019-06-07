from django.contrib import admin
from recommend_service.models import SearchTrail


# Register your models here.

class SearchTrailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'volunteer',
        'time',
    )
    list_per_page = 15


admin.site.register(SearchTrail, SearchTrailAdmin)
