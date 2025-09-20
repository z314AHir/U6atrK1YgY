# 代码生成时间: 2025-09-21 04:56:18
from django.test import TestCase
from django.urls import reverse
from .models import MyModel
from .views import my_view

# 单元测试类
class MyAppTests(TestCase):
    """
    测试My App的单元测试类。
    """
    def setUp(self):
        """
        设置测试环境。
        """
        # 可以在这里创建一些测试数据
        self.test_data = MyModel.objects.create(name="Test Data")

    def test_model(self):
        """
        测试模型是否能够正确保存数据。
        """
        self.assertEqual(MyModel.objects.count(), 1)
        self.assertEqual(self.test_data.name, "Test Data")

    def test_view(self):
        """
        测试视图是否返回正确的响应。
        """
        # 使用reverse获取URL
        url = reverse('my-view')
        # 发送GET请求到视图
        response = self.client.get(url)
        # 检查HTTP响应状态码
        self.assertEqual(response.status_code, 200)

    def test_url(self):
        """
        测试URL是否能够正确解析到视图。
        """
        response = self.client.get(reverse('my-view'))
        self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        """
        测试错误处理机制是否有效。
        """
        # 尝试访问一个不存在的URL
        response = self.client.get('/non-existent-url')
        # 检查是否返回404错误
        self.assertEqual(response.status_code, 404)
