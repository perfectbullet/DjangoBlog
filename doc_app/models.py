from django.db import models


class FileContentFullText(models.Model):
    # 文件内容和文件对应
    id = models.BigAutoField(primary_key=True)
    full_content = models.TextField()
    url = models.CharField(max_length=1024)
    file_path = models.CharField(max_length=1024)

    class Meta:
        managed = True
        db_table = 'file_content_full_text'
