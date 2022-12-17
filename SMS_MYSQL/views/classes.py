from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import ClassesEditModelForm, ClassesModelForm
# Create your views here.

# 采用modelform

from django import forms

# from django.forms import DateInput
#
# class UDateInput(DateInput):
#     input_type = 'date'



def classes_list(request):
    """ 班级列表 """
    data_dict = {}
    search_data =request.GET.get('q', '')
    if search_data:
        data_dict['class_id__contains'] = search_data

    # select  from Table order by level desc;
    queryset = models.Classes.objects.filter(**data_dict).order_by("class_semester")

    return render(request, "classes_list.html", {"queryset": queryset, "search_data": search_data})


# from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
# class PrettyModelForm(BootStrapModelForm):
#     # 验证方式1：正则
#     # mobile = forms.CharField(
#     #     label="手机号",
#     #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误！', ), ]
#     # )
#     class Meta:
#         model = models.PrettyNum
#         fields = "__all__"
#         #exclude = ["level"]
#
#
#     # 钩子方法 验证2
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#
#         if len(txt_mobile) != 11:
#             # 验证不通过
#             raise ValidationError("格式错误！")
#
#         exists_mobile = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
#         if exists_mobile:
#             raise ValidationError("手机号已存在！")
#
#         # pass
#         return txt_mobile

def classes_add(request):
    title = "添加班级信息"
    if request.method == "GET":
        form = ClassesModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = ClassesModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/classes/list")
    else:
        return render(request, "change.html", {"form": form,"title": title})


def classes_edit(request, nid):
    ''' 编辑 '''
    title = "编辑班级信息"
    row_object = models.Classes.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = ClassesEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = ClassesEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/classes/list")

    return render(request, 'change.html', {'form': form, "title": title})


def classes_delete(request, nid):
    models.Classes.objects.filter(id=nid).delete()
    return redirect("/classes/list")

