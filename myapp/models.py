# -*- coding: utf-8 -*-
"""
@Time    : 2022/3/28 13:49
@Author  : soda
@File    : models.py
"""
from django.db import models


# Create your models here.
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
    # phone = models.CharField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

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
