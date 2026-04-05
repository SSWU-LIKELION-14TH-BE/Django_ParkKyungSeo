from django.contrib import admin
from .models import CustomUser, Post, TechStack

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(TechStack) # 기술 스택 항목 관리를 위해 등록