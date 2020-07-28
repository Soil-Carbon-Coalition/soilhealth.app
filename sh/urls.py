from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

# provides a helper function to return a URL pattern for serving files in debug mode:
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admyn/', admin.site.urls),

    # path('account/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('api.urls')),
    # allows login at api root
    path('api-auth/', include('rest_framework.urls')),
    path('', include('frontend.urls')),
    # path('', TemplateView.as_view(template_name="index.html")),
    # path('front/' '/frontend/index.html')

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # this will enable serving images in debug mode by url

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
