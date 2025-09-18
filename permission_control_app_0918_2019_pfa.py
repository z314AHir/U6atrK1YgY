# 代码生成时间: 2025-09-18 20:19:24
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.urls import path

# Models
from django.db import models

class Document(models.Model):
    """Model representing a document."""
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

# Views
class DocumentView(View):
    """View for accessing a document."""
    def get(self, request, *args, **kwargs):
        """Returns the content of a document."""
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        try:
            document = Document.objects.get(pk=kwargs['doc_id'])
            return HttpResponse(document.content)
        except Document.DoesNotExist:
            return HttpResponse("Document not found", status=404)
        except Exception as e:
            return HttpResponse("Error occurred: " + str(e), status=500)

# URLs
document_url = path('document/<int:doc_id>/', login_required(DocumentView.as_view()), name='document')

urlpatterns = [
    document_url,
]

# Example usage:
# from django.urls import include, path
# from . import urls as permission_control_app_urls
# urlpatterns = [
#     path('app/', include(permission_control_app_urls.urlpatterns)),
# ]