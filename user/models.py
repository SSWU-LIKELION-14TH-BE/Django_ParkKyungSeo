from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import migrations, models
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nickname = models.CharField(max_length=50, unique=True, null=True)

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 작성자
    title = models.CharField(max_length=200) # 제목
    content = models.TextField() # 내용
    image = models.ImageField(upload_to='posts/', blank=True, null=True) # 사진 첨부
    created_at = models.DateTimeField(auto_now_add=True) # 작성 시간

    def __str__(self):
        return self.title