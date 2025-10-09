# 代码生成时间: 2025-10-09 18:05:48
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path


# Models
class Payment(models.Model):
    """支付信息模型"""
    order_id = models.CharField(max_length=100, help_text="订单ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="支付金额")
    status = models.CharField(max_length=20, help_text="支付状态")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    def __str__(self):
        return self.order_id


# Views
class PaymentView(View):
    """支付流程处理视图"""
    def post(self, request, *args, **kwargs):
        """处理支付请求"""
        try:
            order_id = request.POST.get('order_id')
            amount = request.POST.get('amount')
            if not order_id or not amount:
                return JsonResponse({'error': 'Missing order_id or amount'}, status=400)
            
            payment, created = Payment.objects.get_or_create(order_id=order_id)
            payment.amount = float(amount)
            payment.status = 'completed'  # 假设支付成功
            payment.save()
            
            return JsonResponse({'message': 'Payment processed successfully', 'order_id': order_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# URLs
urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
]
