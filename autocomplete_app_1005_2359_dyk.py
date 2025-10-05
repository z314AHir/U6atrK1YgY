# 代码生成时间: 2025-10-05 23:59:44
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchRank, SearchQuery

# Model for Autocomplete
class SearchableModel(models.Model):
    searchable_field = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.searchable_field

# View function for Autocomplete
@require_GET  # Ensures that the view only accepts GET requests
@csrf_exempt    # Disable CSRF token for simplicity
def autocomplete(request):
    """
    View function for search autocomplete.
    It takes a query string and returns matching suggestions.
    """
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'suggestions': []})

    # Use Django's PostgreSQL full-text search features
    search_vector = SearchVector('searchable_field')
    search_query = SearchQuery(query)
    results = SearchableModel.objects.annotate(
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.3).order_by('-rank')[:5]

    # Prepare suggestions for the frontend
    suggestions = [item.searchable_field for item in results]
    return JsonResponse({'suggestions': suggestions})

# URL configuration
# Note: Add the following line into your Django app's urls.py file
# path('autocomplete/', views.autocomplete, name='autocomplete')
