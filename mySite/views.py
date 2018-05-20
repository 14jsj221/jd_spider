from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
from django.http import JsonResponse
from captcha.models import CaptchaStore
from . import jdspider

# Create your views here.


def test(request):
    pass
    return render(request, 'login/test.html')


def index(request):
    if request.method == "POST":
        jd_search_form = forms.JDSearchForm(request.POST)
        if jd_search_form.is_valid():
            keyword = jd_search_form.cleaned_data['keyword']
            goods_list = jdspider.get_html(keyword)
            jdspider.write_to_txt(goods_list)
            for item in goods_list:
                t1 = ''.join(item['shop']).strip()
                t2 = ''.join(item['price']).strip()
                t3 = ''.join(item['comments']).strip()
                t4 = ''.join(item['name']).strip()
                t5 = ''.join(item['url'])
                if t1 == '' or t2 == '' or t3 == '' or t4 == '' or t5 == '':
                    continue
                new_info = models.ShopInfo()
                new_info.goods_shop = t1
                new_info.goods_price = t2
                new_info.goods_comments = t3
                new_info.goods_name = t4
                new_info.goods_url = 'https:' + t5
                #new_info.goods_searcher = request.session.user_name
                new_info.save()
            return render(request, 'login/index.html', locals())

    jd_search_form = forms.JDSearchForm()
    return render(request, 'login/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def hash_code(s, salt='jd_spider'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def ajax_val(request):
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(response=request.GET['response'], hashkey=request.GET['hashkey'])
        if cs:
            json_data={'status': 1}
        else:
            json_data = {'status': 0}
        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status': 0}
        return JsonResponse(json_data)


def jd_search(request):
    if request.method == "POST":
        jd_search_form = forms.JDSearchForm(request.POST)
        if jd_search_form.is_valid():
            keyword = jd_search_form.cleaned_data['keyword']
            goods_list = jdspider.get_html(keyword)
            jdspider.write_to_txt(goods_list)

    jd_search_form = forms.JDSearchForm()
    return render(request, 'login/index.html', locals())