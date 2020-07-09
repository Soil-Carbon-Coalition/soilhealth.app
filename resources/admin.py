from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'entered')
    list_filter = ('author', 'project')
    list_select_related = ('project',)
    search_fields = ('title', 'body',)
    view_on_site = True
