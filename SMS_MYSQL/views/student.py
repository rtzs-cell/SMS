from django.db import connection

from django.shortcuts import render, redirect

from SMS_MYSQL import models
from SMS_MYSQL.utils.bootstrap import BootStrapModelForm
from SMS_MYSQL.utils.form import StudentEditModelForm, StudentModelForm
from SMS_MYSQL.utils.raw import custom_sql_get_dict
# Create your views here.

# 采用modelform

from django import forms

# from django.forms import DateInput
#
# class UDateInput(DateInput):
#     input_type = 'date'


def student_list(request):
    """ 学生列表 """
    # data_dict = {}
    # s_id =request.GET.get('q', '')
    # if s_id:
    #     data_dict['student_id__contains'] = s_id
    #
    # # select  from Table order by level desc;
    # queryset = models.Students.objects.filter(**data_dict)

    # 绕过模型层采用原生SQL
    s_id = request.GET.get('s_id', '').strip()
    s_name = request.GET.get('s_name', '').strip()
    s_major = request.GET.get('s_major', '').strip()
    search_data = {
        's_id': s_id,
        's_name': s_name,
        's_major': s_major
    }
    ALL = "select A.id,student_id,student_name, student_gender, student_birthday, classes_id \
                from sms_mysql_students A, sms_mysql_classes B, sms_mysql_majors C \
                where A.classes_id = B.class_id and B.majors_id = C.major_id"
    sql_cmd = ALL
    if s_id:
        sql_cmd = sql_cmd + " and A.student_id = '%s' " % s_id

    if s_name:
         sql_cmd = sql_cmd + " and A.student_name = '%s' " % s_name

    if s_major:
        sql_cmd = sql_cmd + " and C.major_name = '%s' " % s_major

    querydict = custom_sql_get_dict(sql_cmd)
    # print(sql_cmd)

    for d in querydict:
        #print(d)
        if d['student_gender'] == 1:
            d['student_gender'] = '男'
        else:
            d['student_gender'] = '女'
    #print(querydict)

    # 查询结果一摸一样!
    # queryset = models.Students.objects.all()
    # print(queryset.values())
    return render(request, "student_list.html", {"queryset": querydict, "search_data": search_data})


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

def student_add(request):
    title = "添加学生信息"
    if request.method == "GET":
        form = StudentModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    #POST收到
    form = StudentModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/student/list")
    else:
        return render(request, "change.html", {"form": form, "title": title})


def student_edit(request, nid):
    ''' 编辑 '''
    title = "编辑学生信息"
    row_object = models.Students.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = StudentEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    # POST

    form = StudentEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/student/list")

    return render(request, 'change.html', {'form': form, "title": title})


def student_delete(request, nid):
    models.Students.objects.filter(id=nid).delete()
    return redirect("/student/list")