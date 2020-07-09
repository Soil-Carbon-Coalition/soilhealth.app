from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q


from obs.models import Observation


class SearchResultsView(ListView):
    model = Observation
    template_name = 'search/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Observation.objects.filter(
            Q(kv__icontains=query)
        )
