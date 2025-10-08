# 代码生成时间: 2025-10-08 23:12:51
from django.apps import AppConfig
from django.db import models
from django.views import View
from django.urls import path
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# Define the Metadata model
class Metadata(models.Model):
    """
    Represents a metadata item with a key and a value.
    """
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


# Define a view to handle metadata CRUD operations
class MetadataView(View):
    """
    A view to manage metadata items.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        """
        Creates a new metadata item.
        """
        key = request.POST.get('key')
        value = request.POST.get('value')
        if not key or not value:
            return HttpResponseBadRequest('Key and value are required.')

        metadata = Metadata.objects.create(key=key, value=value)
        return JsonResponse({'id': metadata.id, 'key': metadata.key, 'value': metadata.value})

    def get(self, request, *args, **kwargs):
        """
        Retrieves all metadata items.
        """
        metadata_items = Metadata.objects.all()
        data = [{'id': item.id, 'key': item.key, 'value': item.value} for item in metadata_items]
        return JsonResponse({'metadata': data}, safe=False)

    def put(self, request, *args, **kwargs):
        """
        Updates an existing metadata item.
        """
        key = request.PUT.get('key')
        value = request.PUT.get('value')
        metadata = Metadata.objects.filter(key=key).first()
        if not metadata:
            return HttpResponseBadRequest('Metadata not found.')

        metadata.value = value
        metadata.save()
        return JsonResponse({'key': metadata.key, 'value': metadata.value})

    def delete(self, request, *args, **kwargs):
        """
        Deletes a metadata item.
        """
        key = request.DELETE.get('key')
        metadata = Metadata.objects.filter(key=key).first()
        if metadata:
            metadata.delete()
            return JsonResponse({'status': 'Metadata deleted successfully.'})
        else:
            return HttpResponseBadRequest('Metadata not found.')

# Define the URL patterns for the view
metadata_patterns = [
    path('metadata/', MetadataView.as_view(), name='metadata'),
]

class MetadataManagementConfig(AppConfig):
    """
    AppConfig for the metadata management application.
    """
    name = 'metadata_management'
    verbose_name = 'Metadata Management'