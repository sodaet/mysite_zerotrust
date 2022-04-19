# -*- coding: utf-8 -*-
"""
@Time    : 2022/3/28 15:41
@Author  : soda
@File    : admin.py
"""
from django.contrib import admin

# Register your models here.

from . import models
from .models import ArticlePost

admin.site.register(models.User)  # 简单的注册模型
admin.site.register(models.ConfirmString)
admin.site.register(ArticlePost)
