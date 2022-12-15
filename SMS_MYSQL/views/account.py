from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse
from django import forms

from SMS_MYSQL.utils.encrypt import md5
from SMS_MYSQL import models
from SMS_MYSQL.utils.captcha_check import captcha_check



class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={
            "placeholder": "用户名"
        }),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "placeholder": "密码"
            }
        ),
        required=True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={
                "placeholder": "验证码",
                "autocomplete": "off",
            }
        ),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """登录界面"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码校验
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code")

        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误！")
            return render(request, "login.html", {'form': form})

        # 验证成功
        # print(form.cleaned_data)
        # 去数据库校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # print("验证失败")
            form.add_error("password", "用户名或密码错误！")
            return render(request, "login.html", {'form': form})

        #用户名和密码正确
        #网站生成随机字符串写到用户浏览器的cookie中，然后写到相应的session中
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        # 设置七天免登录
        request.session.set_expiry(60*60*24*7)
        return redirect("/admin/list/")


    return render(request, "login.html", {'form': form})


def logout(request):

    request.session.clear()
    form = LoginForm()
    return render(request, "login.html", {"form": form})


def image_code(request):
    img, chr_4 = captcha_check()
    #print(img, chr_4)
    stream = BytesIO()
    img.save(stream, 'png')

    #写入到自己的session中以便后续校验
    request.session["image_code"] = chr_4
    #给Session设置60s超时
    request.session.set_expiry(60)


    return HttpResponse(stream.getvalue())
