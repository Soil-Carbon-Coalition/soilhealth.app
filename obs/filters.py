def filter_site_observations(queryset, request, prefix=None):
    filters = ['project_id', 'observer_id', 'obs_type_id', 'kv__icontains']
    for f in filters:
        val = request.query_params.get(f)
        if val:
            if prefix:
                kwargs = {'%s__%s' % (prefix, f): val}
            else:
                kwargs = {f: val}
            queryset = queryset.filter(**kwargs)
    return queryset
