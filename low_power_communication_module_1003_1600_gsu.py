# 代码生成时间: 2025-10-03 16:00:58
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import logging

# Create your models here.
class Message(models.Model):
    """Model to store messages for low power communication."""
    message_id = models.AutoField(primary_key=True)
    message = models.TextField(help_text="The message content.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id}"

# Create your views here.
class LowPowerMessageView(View):
    """View to handle messages using low power communication protocol."""
    def post(self, request, *args, **kwargs):
        """Handle POST request to send a low power message."""
        try:
            message_content = request.POST.get('message')
            if not message_content:
                return JsonResponse({'error': 'Message content is required.'}, status=400)

            new_message = Message.objects.create(message=message_content)
            return JsonResponse({'message_id': new_message.message_id}, status=201)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return JsonResponse({'error': 'Internal server error.'}, status=500)

# Create your urls here.
urlpatterns = [
    path('send/', LowPowerMessageView.as_view(), name='send_message'),
]
