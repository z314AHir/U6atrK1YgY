# 代码生成时间: 2025-10-05 03:11:27
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Models
class Resource(models.Model):
    """Model representing a healthcare resource."""
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Views
class ResourceListView(View):
    """View for listing and creating healthcare resources."""
    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request):
        resources = Resource.objects.all()
        return JsonResponse([resource.__dict__ for resource in resources], safe=False)

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            new_resource = Resource.objects.create(
                name=request.POST['name'],
                type=request.POST['type'],
                location=request.POST['location'],
                available=True
            )
            return JsonResponse(new_resource.__dict__, safe=False)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)

class ResourceDetailView(View):
    """View for retrieving, updating, and deleting a healthcare resource."""
    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk)
            return JsonResponse(resource.__dict__, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Resource not found'}, status=404)

    @method_decorator(csrf_exempt, name='dispatch')
    def put(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk)
            resource.name = request.PUT.get('name', resource.name)
            resource.type = request.PUT.get('type', resource.type)
            resource.location = request.PUT.get('location', resource.location)
            resource.available = request.PUT.get('available', resource.available)
            resource.save()
            return JsonResponse(resource.__dict__, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Resource not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)

    @method_decorator(csrf_exempt, name='dispatch')
    def delete(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk)
            resource.delete()
            return JsonResponse({'message': 'Resource deleted'}, status=204)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Resource not found'}, status=404)

# URL Patterns
urlpatterns = [
    path('resources/', ResourceListView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
]
