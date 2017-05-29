from haystack.generic_views import SearchView as HaystackSearchView


class SearchView(HaystackSearchView):
    template = 'search/search.html'
    context_object_name = 'products'
