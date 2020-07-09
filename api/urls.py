from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
app_name = 'api'

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'observations', views.ObservationViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'maps', views.MapViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'resources', views.ResourceViewSet)
router.register(r'status', views.UserStatusViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls',
    #   namespace='rest_framework')),
    path('register/', views.registration_view, name='register'),
    # path('token', TokenObtainPairView.as_view()), # for JWT
    # path('token/refresh', TokenRefreshView.as_view()), # for JWT
    path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('user/current/', views.CurrentUserView.as_view(), name='current_user'),

]
# Vincent uses this, but with default json renderer it's not needed perhaps
# urlpatterns = format_suffix_patterns(urlpatterns)