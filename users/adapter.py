from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class SHAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/api/projects/{default_project}/"
        return path.format(default_project=request.user.default_project_id)
