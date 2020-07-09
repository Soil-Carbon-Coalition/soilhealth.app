from django.contrib import admin
from django.contrib.gis import admin
# from django.contrib.sites import Site as AuthSite
from leaflet.admin import LeafletGeoAdmin
from .models import Site, Observation, Project, ObservationType, PointSite
from maps.models import Map, RasterLayer, VectorLayer
from django.contrib.postgres import fields
# from django_json_widget.widgets import JSONEditorWidget
from django.contrib.auth.models import Group

admin.site.unregister(Group)


admin.site.site_header = "SOILHEALTH.APP admin dashboard"
admin.site.register(Site, LeafletGeoAdmin)
admin.site.register(ObservationType)
admin.site.register(Project)
admin.site.register(RasterLayer)
admin.site.register(VectorLayer)
admin.site.register(PointSite, LeafletGeoAdmin)
# admin.site.unregister(AuthSite)


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    filter_horizontal = ['rasters', 'vectors']


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     fields.JSONField: {
    #         'widget': JSONEditorWidget
    #     },
    # }
    raw_id_fields = ['parentobs']
    list_filter = ('observer', 'site', 'project', 'type')
    list_select_related = ('observer', 'site', 'project', 'type')
    search_fields = ('kv',)
    view_on_site = True


'''
This might enable filtering of admin for project coordinators
'''

# def queryset(self, request):
#     qs = super(ObservationAdmin, self).queryset(request)
#     if request.user.is_superuser:
#         return qs
#     # this could be Project Coordinator instead of observer
#     return qs.filter(observer=request.user)

# @admin.register(RasterLayer)
# class RasterLayerAdmin(admin.ModelAdmin):
# formfield_overrides = {
#     fields.JSONField: {
#         'widget': JSONEditorWidget
#     },
# }

# @admin.register(VectorLayer)
# class VectorLayerAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         fields.JSONField: {
#             'widget': JSONEditorWidget
#         },
