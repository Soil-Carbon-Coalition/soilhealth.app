from django.contrib.sessions.models import Session
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.gis import admin
from django.contrib.postgres import fields
# from django.contrib.sites import Site as AuthSite
from leaflet.admin import LeafletGeoAdmin
from .models import Site, Observation, Project, ObservationType
from maps.models import Map, RasterLayer, VectorLayer
from users.models import CustomUser, UserStatus
from posts.models import Post, PostComment
# from django_json_widget.widgets import JSONEditorWidget
from django.contrib.auth.models import Group

# admin.site.unregister(Group)


admin.site.site_header = "SOILHEALTH.APP admin dashboard"
admin.site.register(Site)
admin.site.register(ObservationType)
admin.site.register(RasterLayer)
admin.site.register(VectorLayer)
# admin.site.register(LeafletGeoAdmin)
# admin.site.unregister(AuthSite)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    filter_horizontal = ['rasters', 'vectors']


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):

    list_filter = (
        ('project', RelatedOnlyFieldListFilter),
        ('observer', RelatedOnlyFieldListFilter),
        ('site', RelatedOnlyFieldListFilter),
        ('obs_type', RelatedOnlyFieldListFilter),
    )
    list_select_related = ('observer', 'site', 'project', 'obs_type')
    search_fields = ('kv',)
    view_on_site = True

    def get_queryset(self, request):
        ''' restrict observation list to projects for which request.user is coordinator;
        request.user may be coordinator of more than one project '''
        obs = super(ObservationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return obs
        projects = UserStatus.objects.filter(
            user_status="CO").filter(user=request.user)
        projects = [us.project_id for us in projects]
        return obs.filter(project_id__in=projects)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        ''' restrict project list to coordinator's own projects.'''
        projs = super(ProjectAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return projs
        projects = UserStatus.objects.filter(
            user_status="CO").filter(user=request.user)
        projects = [us.project_id for us in projects]
        return projs.filter(id__in=projects)
