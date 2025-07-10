from django.utils.cache import add_never_cache_headers

def no_cache(view_func):
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        add_never_cache_headers(response)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return _wrapped_view
