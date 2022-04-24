# -*- coding: utf-8 -*-
"""
@Time    : 2022/3/28 13:49
@Author  : soda
@File    : models.py
"""
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    """
    用户信息表
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, unique=True, default="")
    sex = models.CharField(max_length=32, choices=gender, default="男")
    serial_number = models.CharField(max_length=128, unique=True, default="")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = "用户"  # 就是给我们的模型起一个中文的名字
        verbose_name_plural = "用户"  # 表示复数形式显示，如果不指定，django就会在我们的“用户”后面加一个s


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title
