from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'entered')
    list_filter = ('author', 'project')
    list_select_related = ('project',)
    search_fields = ('title', 'body',)
    view_on_site = True

    def get_queryset(self, request):
        ''' restrict post list to coordinator's own projects.'''
        posts = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return posts
        projects = UserStatus.objects.filter(
            user_status="CO").filter(user=request.user)
        projects = [us.project_id for us in projects]
        return posts.filter(id__in=projects)
