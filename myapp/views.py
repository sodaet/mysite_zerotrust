# -*- coding: utf-8 -*-
"""
@Time    : 2022/3/28 16:44
@Author  : soda
@File    : views.py
"""
import datetime
import hashlib
import re

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse

# Create your views here.
from markdown import markdown

from myapp import models, forms
from myapp.models import ArticlePost


def login(request):
    # 登录
    # if reverse('/login/'):
    #     return render(request, 'login.html')
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form:
            username = request.POST.get("username")
            password = request.POST.get("password")
            try:
                user = models.User.objects.get(name=username)
                print(user.has_confirmed)
            except:
                message = "username or passwd not right....\nplease rewrite...."
                return render(request, 'login.html', locals())
            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = "username or passwd not right....\nplease rewrite...."
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def index(request):
    # 主页视图
    # if reverse('/index/'):
    #     return render(request, 'index.html')
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'index.html', context)


def register(request):
    # 注册视图
    # if reverse('/register/'):
    #     return render(request, 'register.html')
    if request.session.get("is_login", None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():  # 判断表单的数据是否合法，返回一个布尔值
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            phone = register_form.cleaned_data.get('phone')
            sex = register_form.cleaned_data.get('sex')

            # 使用正则验证手机号
            flag = re.search(r"1[3|4|5|7|8][0-9]{9}", phone)

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            elif not flag:
                message = '手机号码不对'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名或密码错误'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.phone = phone
                new_user.save()
                code = make_confirm_string(new_user)
                send_email(email, code)
                message = '请前往邮箱进行确认！'
                return render(request, 'confirm.html', locals())
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    # 登出视图
    # if reverse('/logout/'):
    #     return render(request, 'login.html')
    # print("logout: " + request.get_full_path())
    if not request.session.get("is_login", None):  # get没有值返回None
        return redirect('/login/')
    request.session.flush()  # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    return redirect('/login/')


def article_detail(request, id):
    article = get_object_or_404(ArticlePost, id=id)
    # 引入markdown
    article.body = markdown(article.body,
                            extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                            ])
    context = {'article': article}
    return render(request, 'detail.html', context)


def hash_code(s, salt='LogAndReg'):  # hash
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自soda的零信任的登录注册系统的注册确认邮件'

    text_content = '''感谢注册零信任的登录注册系统，这里是soda发送的邮件\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>零信任的登录注册系统</a>，\
                    这里是soda发送的邮件</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())


def user_profile(request):
    userinfo = models.User.objects.get(id=request.session.get("user_id"))
    context = {'userinfo': userinfo}
    print("123", context)
    return render(request, 'showme.html', context)
