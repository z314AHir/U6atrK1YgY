# 代码生成时间: 2025-09-29 14:56:51
from django.apps import AppConfig
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import path
from django.views import View, generic
from django.http import JsonResponse
import json
import logging

# 配置应用名称
class ServiceDiscoveryAppConfig(AppConfig):
    name = 'service_discovery_app'

# 服务发现和注册模型
class Service(models.Model):
    """
    服务发现模型，记录服务名称，服务地址等信息。
    """
    name = models.CharField(max_length=255, unique=True, help_text="服务名称")
    address = models.CharField(max_length=255, help_text="服务地址")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '服务'
        verbose_name_plural = '服务'

# 服务视图
class ServiceView(View):
    """
    服务发现和注册视图。
    """
    def post(self, request, *args, **kwargs):
        """
        处理服务注册请求。
        """
        try:
            data = json.loads(request.body)
            name = data.get('name')
            address = data.get('address')

            # 验证数据
            if not name or not address:
                raise ValidationError('服务名称和服务地址不能为空')

            # 注册服务
            service, created = Service.objects.get_or_create(name=name, defaults={'address': address})
            return JsonResponse({'status': 'success', 'message': '服务注册成功' if created else '服务已存在'}, status=201)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '请求体格式错误'}, status=400)

    def get(self, request, *args, **kwargs):
        """
        处理服务发现请求。
        """
        try:
            services = Service.objects.all()
            services_data = list(services.values('name', 'address'))
            return JsonResponse({'status': 'success', 'data': services_data}, status=200)
        except Exception as e:
            logging.error(f'服务发现失败：{str(e)}')
            return JsonResponse({'status': 'error', 'message': '服务发现失败'}, status=500)

# URL配置
urlpatterns = [
    path('register/', ServiceView.as_view(), name='register'),
    path('discover/', ServiceView.as_view(), name='discover'),
]
