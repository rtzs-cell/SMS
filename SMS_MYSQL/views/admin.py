from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
from django.core.validators import ValidationError

from SMS_MYSQL import models
from SMS_MYSQL.utils import page
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.encrypt import md5


def admin_list(request):
    """管理员列表"""

    #search
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['username__contains'] = search_data

    #根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    ###############    分页组件固定用法     #############
    current_page = request.GET.get('page')
    page_object = page.Pagination(current_page=current_page,
                                  all_count=queryset.count(),
                                  base_url=request.path_info,
                                  query_params=request.GET,
                                  per_page=10,
                                  )
    queryset = models.Admin.objects.all()[page_object.start:page_object.end]
    page_html = page_object.page_html()
    # 'page_html': page_html
    return render(request, "admin_list.html", {'queryset': queryset, 'page_html': page_html})


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        #print('pwd', pwd)
        return md5(pwd)

    def clean_confirm_password(self):
        first_password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        #print('cp',confirm_password)
        confirm_password = md5(confirm_password)

        if confirm_password != first_password:
            return ValidationError('密码不一致！')

        # 此字段返回什么数据库就是什么
        return confirm_password


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


def admin_add(request):
    """新建管理员"""
    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, "change.html", {'title': title, 'form': form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {'title': title, 'form': form})


def admin_edit(request, nid):
    """编辑管理员"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在!"})

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title })

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"form": form, "title": title})

def admin_delete(request, nid):
    exists = models.Admin.objects.filter(id=nid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "数据不存在！"})

    models.Admin.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})
    #return redirect("/admin/list")


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        #print('pwd', pwd)
        return md5(pwd)

    def clean_confirm_password(self):
        first_password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        #print('cp',confirm_password)
        confirm_password = md5(confirm_password)

        if confirm_password != first_password:
            return ValidationError('密码不一致！')

        # 此字段返回什么数据库就是什么
        return confirm_password


def admin_reset(request, nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在!"})

    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})

