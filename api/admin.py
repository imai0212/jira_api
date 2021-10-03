from django.contrib import admin
from .models import Category, Task, Profile
# models.pyの特定モデルをadminサイトに登録
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Profile)
