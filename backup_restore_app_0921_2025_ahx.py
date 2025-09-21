# 代码生成时间: 2025-09-21 20:25:23
from django.db import models, migrations
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
from django.utils.decorators import method_decorator
import json
import os
import shutil
import tempfile

# 定义备份/恢复的模型
class Backup(models.Model):
    file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=10, choices=(('backup', 'Backup'), ('restore', 'Restore')))

    def __str__(self):
        return f"{self.operation} - {self.created_at}"

# 定义视图
@method_decorator(require_http_methods(['POST']), name='dispatch')
class BackupRestoreView(models.Model):
    def backup(self, request):
        """
        创建数据库备份
        """
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = os.path.join(tmpdir, 'db_backup.sql')
                call_command('dumpdata', output=file_path)
                backup = Backup.objects.create(file_path=file_path, operation='backup')
                return JsonResponse({'file_path': backup.file_path}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def restore(self, request):
        """
        恢复数据库备份
        """
        try:
            backup_file = request.FILES.get('file')
            if not backup_file.name.endswith('.sql'):
                raise ValueError('Invalid file format. Only .sql files are allowed.')
            with tempfile.TemporaryDirectory() as tmpdir:
                file_path = os.path.join(tmpdir, backup_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in backup_file.chunks():
                        destination.write(chunk)
                call_command('loaddata', file_path)
                backup = Backup.objects.create(file_path=file_path, operation='restore')
                return JsonResponse({'file_path': backup.file_path}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# 定义URL配置
urlpatterns = [
    # 备份数据库
    path('backup/', BackupRestoreView.as_view(action='backup'), name='backup'),
    # 恢复数据库
    path('restore/', BackupRestoreView.as_view(action='restore'), name='restore'),
]

# 错误处理
def error_500(request):
    """
    500错误处理
    """
    return JsonResponse({'error': 'Internal Server Error'}, status=500)

# 配置错误处理
handler500 = 'backup_restore_app.views.error_500'