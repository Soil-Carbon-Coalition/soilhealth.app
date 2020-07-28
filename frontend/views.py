from django.shortcuts import render
from django.views.generic import TemplateView

# Serve Vue Application
from django.views.decorators.cache import never_cache

index_view = never_cache(TemplateView.as_view(
    template_name='frontend/index.html'))


# def index(request):
#     return render(request, 'frontend/index.html')
