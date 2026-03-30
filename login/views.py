import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import RegisterUser
from django.conf import settings
from django.template.exceptions import TemplateDoesNotExist



def dynamic_user_page(request, page):
    try:
        return render(request, f'user/{page}.html')  # 页面在 templates/ 目录下平行存放
    except TemplateDoesNotExist:
        return render(request, 'user/404.html', status=404)
    

# 登录视图
def login(request):
    if request.method == "GET":
        return render(request, "user/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = RegisterUser.objects.get(username=username)
            salted_password = password + settings.SECRET_KEY
            hashed_password = hashlib.md5(salted_password.encode("utf-8")).hexdigest()
            if hashed_password == user.password:
                request.session['username'] = user.username
                return redirect('/user/index')
            else:
                return HttpResponse("<h1>密码错误</h1>重新登录")
        except RegisterUser.DoesNotExist:
            return HttpResponse("<h1>用户名不存在</h1>重新登录")

# 注册视图
def register(request):
    return render(request, 'user/register.html')

# 首页视图
def index(request):
    username = request.session.get('username')
    return render(request, "user/index.html", context={"username": username})

# 页面 2
def smart(request):
    return render(request, 'user/smart.html')

# 模型预测页
def model_prediction(request):
    return render(request, 'user/model-prediction.html')

# 搜索页
def search(request):
    return render(request, 'user/search.html')

# 动态加载页面（备用）
def dynamic_page(request, page_name):
    if page_name == 'smart':
        return render(request, 'user/smart.html')
    else:
        return render(request, '404.html', status=404)