# -*- coding: utf-8 -*-
"""
@Time    : 2022/3/29 10:34
@Author  : soda
@File    : forms.py
"""
from django import forms
from captcha.fields import CaptchaField
from django.core.validators import RegexValidator


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label="验证码")


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ("female", "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号码", max_length=16,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    serial_number = forms.CharField(label="设备编号", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


# class UserInfo(forms.Form):
#     username = forms.CharField(label="用户名")
#     email = forms.CharField(label="邮箱地址")
#     phone = forms.CharField(label="电话号码")
#     sex = forms.CharField(label="性别")
#     confirmed = forms.CharField(label="邮件确认")
