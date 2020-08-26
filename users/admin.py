from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserStatus
from obs.models import Project
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(DjangoUserAdmin):
    """Define admin model for CustomUser model with no username field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
         'fields': ('full_name', 'user_location', 'default_project')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('full_name', 'email', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('project', 'user_status', 'user')
    list_filter = ('user_status', 'user')

    # CAN WE FILTER THE OPTION LIST TO PROJECT THAT USER IS CO WITH?
    def get_queryset(self, request):
        ''' restrict project list to coordinator's own projects.'''
        userstatuses = super(UserStatusAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return userstatuses
        projects = UserStatus.objects.filter(
            user_status="CO").filter(user=request.user)
        projects = [us.project_id for us in projects]
        return userstatuses.filter(project_id__in=projects)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        this filters the Project selector so that project coordinators
        cannot appoint themselves coordinators of other projects
        '''
        if request.user.is_superuser:
            return super(UserStatusAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'project':
            projects = UserStatus.objects.filter(
                user_status="CO").filter(user=request.user)
            projects = [us.project_id for us in projects]
            kwargs["queryset"] = Project.objects.filter(
                id__in=projects)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
