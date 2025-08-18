from django.db import models
import uuid
import os
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # 원본 파일명 저장
        instance.original_filename = filename  

        # 중복 방지를 위해 uuid로 실제 저장 파일명 변경
        ext = filename.split('.')[-1]
        filename = f'{uuid.uuid4().hex}.{ext}'
        return os.path.join(self.sub_path, filename)


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    content = models.TextField()
    upload = models.FileField(
        upload_to=UploadToPathAndRename('uploads/'),
        blank=True,
        null=True
    )
    # 원본 파일명 저장용
    original_filename = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
