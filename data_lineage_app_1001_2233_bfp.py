# 代码生成时间: 2025-10-01 22:33:32
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django import forms
from django.core.exceptions import ValidationError

# Models
class DataSource(models.Model):
    """Model representing a data source."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class DataFlow(models.Model):
    """Model representing a data flow between data sources."""
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='outgoing_flows')
    target = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='incoming_flows')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.source.name} -> {self.target.name}"

# Forms
class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = ['name', 'description']

# Views
class DataSourceListView(View):
    """View to list all data sources."""
    def get(self, request, *args, **kwargs):
        sources = DataSource.objects.all().values()
        return JsonResponse(list(sources), safe=False)

class DataSourceCreateView(View):
    """View to create a new data source."""
    def post(self, request, *args, **kwargs):
        form = DataSourceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Data source created successfully.'}, status=201)
        return JsonResponse(form.errors, status=400)

class DataFlowCreateView(View):
    """View to create a new data flow."""
    def post(self, request, *args, **kwargs):
        # Assuming request data is in the format: { 'source_id': ..., 'target_id': ..., 'description': ... }
        source_id = request.POST.get('source_id')
        target_id = request.POST.get('target_id')
        description = request.POST.get('description')
        try:
            source = DataSource.objects.get(id=source_id)
            target = DataSource.objects.get(id=target_id)
            DataFlow.objects.create(source=source, target=target, description=description)
            return JsonResponse({'message': 'Data flow created successfully.'}, status=201)
        except DataSource.DoesNotExist:
            return JsonResponse({'error': 'One of the data sources does not exist.'}, status=404)

# URLs
app_name = 'data_lineage'
urlpatterns = [
    path('sources/', DataSourceListView.as_view(), name='source-list'),
    path('sources/create/', DataSourceCreateView.as_view(), name='source-create'),
    path('flows/create/', DataFlowCreateView.as_view(), name='flow-create'),
]
