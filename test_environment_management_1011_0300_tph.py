# 代码生成时间: 2025-10-11 03:00:26
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import path
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages

# Models
class TestEnvironment(models.Model):
    """Model to represent a test environment."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Views
class TestEnvironmentListView(ListView):
    """View to list all test environments."""
    model = TestEnvironment
    template_name = 'test_env_list.html'
    context_object_name = 'test_environments'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TestEnvironmentCreateView(CreateView):
    """View to create a new test environment."""
    model = TestEnvironment
    template_name = 'test_env_form.html'
    fields = ['name', 'description']
    success_url = '/test_environments/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TestEnvironmentUpdateView(UpdateView):
    """View to update an existing test environment."""
    model = TestEnvironment
    template_name = 'test_env_form.html'
    fields = ['name', 'description']
    success_url = '/test_environments/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TestEnvironmentDeleteView(DeleteView):
    """View to delete a test environment."""
    model = TestEnvironment
    template_name = 'test_env_confirm_delete.html'
    success_url = '/test_environments/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# URLs
urlpatterns = [
    path('test_environments/', TestEnvironmentListView.as_view(), name='test_environment_list'),
    path('test_environments/new/', TestEnvironmentCreateView.as_view(), name='test_environment_new'),
    path('test_environments/<int:pk>/edit/', TestEnvironmentUpdateView.as_view(), name='test_environment_edit'),
    path('test_environments/<int:pk>/delete/', TestEnvironmentDeleteView.as_view(), name='test_environment_delete'),
]
