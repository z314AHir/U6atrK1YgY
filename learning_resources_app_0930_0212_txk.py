# 代码生成时间: 2025-09-30 02:12:23
from django.db import models
from django.views import View
from django.http import JsonResponse, Http404
from django.urls import path
from django.shortcuts import render


# models.py
class Resource(models.Model):
    """学习资源模型"""
    title = models.CharField(max_length=255, verbose_name="标题")
    description = models.TextField(verbose_name="描述")
    link = models.URLField(verbose_name="链接")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
# 增强安全性
        return self.title


# views.py
class ResourceListView(View):
    """学习资源列表视图"""
    def get(self, request, *args, **kwargs):
# 添加错误处理
        resources = Resource.objects.all()
        return render(request, 'learning_resources/resource_list.html', {'resources': resources})
# NOTE: 重要实现细节


class ResourceDetailView(View):
    """学习资源详情视图"""
    def get(self, request, pk, *args, **kwargs):
        try:
            resource = Resource.objects.get(pk=pk)
            return render(request, 'learning_resources/resource_detail.html', {'resource': resource})
        except Resource.DoesNotExist:
            raise Http404('学习资源不存在')


# urls.py
app_name = 'learning_resources'
urlpatterns = [
g    path('', ResourceListView.as_view(), name='resource_list'),
g    path('<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
]
